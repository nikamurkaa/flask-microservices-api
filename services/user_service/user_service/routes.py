from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from .schemas import require_json_object, validate_user_payload
from .storage import user_store

users_bp = Blueprint("users", __name__)


@users_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "user-service"}), 200


@users_bp.post("/users")
def create_user():
    if not request.is_json:
        raise BadRequest("Expected application/json request body")

    payload = require_json_object(request.get_json(silent=True))
    name, email = validate_user_payload(payload)
    user = user_store.create(name=name, email=email)

    return jsonify(user.to_dict()), 201


@users_bp.get("/users")
def list_users():
    return jsonify([user.to_dict() for user in user_store.list_all()]), 200


@users_bp.get("/users/<int:user_id>")
def get_user(user_id: int):
    user = user_store.get(user_id)
    if user is None:
        raise NotFound(f"User with id={user_id} was not found")

    return jsonify(user.to_dict()), 200
