from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound, ServiceUnavailable

from .clients import fetch_user, get_request_timeout, get_user_service_url
from .schemas import require_json_object, validate_order_payload
from .storage import order_store

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "order-service"}), 200


@orders_bp.get("/ready")
def readiness_check():
    try:
        fetch_user(1)
    except BadRequest:
        return (
            jsonify(
                {
                    "status": "ok",
                    "service": "order-service",
                    "dependencies": {"user-service": "reachable"},
                }
            ),
            200,
        )
    except ServiceUnavailable as exc:
        raise ServiceUnavailable("User service is not reachable") from exc

    return (
        jsonify(
            {
                "status": "ok",
                "service": "order-service",
                "dependencies": {"user-service": "reachable"},
            }
        ),
        200,
    )


@orders_bp.get("/config")
def get_runtime_config():
    return (
        jsonify(
            {
                "user_service_url": get_user_service_url(),
                "request_timeout_seconds": get_request_timeout(),
            }
        ),
        200,
    )


@orders_bp.post("/orders")
def create_order():
    if not request.is_json:
        raise BadRequest("Expected application/json request body")

    payload = require_json_object(request.get_json(silent=True))
    user_id, item, price = validate_order_payload(payload)
    user = fetch_user(user_id)

    order = order_store.create(
        user_id=user_id,
        item=item,
        price=price,
        user_name=user["name"],
        user_email=user["email"],
    )

    return jsonify(order.to_dict()), 201


@orders_bp.get("/orders")
def list_orders():
    return jsonify([order.to_dict() for order in order_store.list_all()]), 200


@orders_bp.get("/orders/<int:order_id>")
def get_order(order_id: int):
    order = order_store.get(order_id)
    if order is None:
        raise NotFound(f"Order with id={order_id} was not found")

    return jsonify(order.to_dict()), 200
