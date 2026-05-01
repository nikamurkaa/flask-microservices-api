from __future__ import annotations

from typing import Any

from werkzeug.exceptions import BadRequest

MAX_ITEM_LENGTH = 200


def require_json_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise BadRequest("Request body must be a JSON object")
    return payload


def validate_order_payload(payload: dict[str, Any]) -> tuple[int, str, float]:
    user_id = payload.get("user_id")
    item = payload.get("item")
    price = payload.get("price")

    if not isinstance(user_id, int) or user_id <= 0:
        raise BadRequest("Field 'user_id' must be a positive integer")

    if not isinstance(item, str) or not item.strip():
        raise BadRequest("Field 'item' must be a non-empty string")
    item = item.strip()
    if len(item) > MAX_ITEM_LENGTH:
        raise BadRequest(f"Field 'item' must be at most {MAX_ITEM_LENGTH} characters")

    if isinstance(price, bool) or not isinstance(price, (int, float)) or price <= 0:
        raise BadRequest("Field 'price' must be a positive number")

    return user_id, item, float(price)
