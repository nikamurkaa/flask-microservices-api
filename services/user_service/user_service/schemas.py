from __future__ import annotations

import re
from typing import Any

from werkzeug.exceptions import BadRequest

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_NAME_LENGTH = 120
MAX_EMAIL_LENGTH = 254


def require_json_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise BadRequest("Request body must be a JSON object")
    return payload


def validate_user_payload(payload: dict[str, Any]) -> tuple[str, str]:
    name = payload.get("name")
    email = payload.get("email")

    if not isinstance(name, str) or not name.strip():
        raise BadRequest("Field 'name' must be a non-empty string")
    if len(name.strip()) > MAX_NAME_LENGTH:
        raise BadRequest(f"Field 'name' must be at most {MAX_NAME_LENGTH} characters")

    if not isinstance(email, str) or not email.strip():
        raise BadRequest("Field 'email' must be a non-empty string")
    email = email.strip().lower()
    if len(email) > MAX_EMAIL_LENGTH or not EMAIL_RE.match(email):
        raise BadRequest("Field 'email' must be a valid email address")

    return name.strip(), email
