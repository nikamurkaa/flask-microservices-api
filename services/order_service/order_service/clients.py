from __future__ import annotations

import os
from typing import Any

import requests
from werkzeug.exceptions import BadRequest, BadGateway, ServiceUnavailable

DEFAULT_USER_SERVICE_URL = "http://127.0.0.1:5001"
DEFAULT_REQUEST_TIMEOUT = 2.0


def get_user_service_url() -> str:
    return os.getenv("USER_SERVICE_URL", DEFAULT_USER_SERVICE_URL).rstrip("/")


def get_request_timeout() -> float:
    raw_timeout = os.getenv("REQUEST_TIMEOUT_SECONDS")
    if raw_timeout is None:
        return DEFAULT_REQUEST_TIMEOUT

    try:
        timeout = float(raw_timeout)
    except ValueError:
        return DEFAULT_REQUEST_TIMEOUT

    return timeout if timeout > 0 else DEFAULT_REQUEST_TIMEOUT


def fetch_user(user_id: int) -> dict[str, Any]:
    url = f"{get_user_service_url()}/users/{user_id}"

    try:
        response = requests.get(url, timeout=get_request_timeout())
    except requests.exceptions.RequestException as exc:
        raise ServiceUnavailable("User service is unavailable") from exc

    if response.status_code == 404:
        raise BadRequest(f"User with id={user_id} does not exist")
    if response.status_code >= 500:
        raise ServiceUnavailable("User service returned a server error")
    if response.status_code != 200:
        raise BadGateway("User service returned an unexpected response")

    try:
        user = response.json()
    except ValueError as exc:
        raise BadGateway("User service returned invalid JSON") from exc

    if not isinstance(user, dict) or "name" not in user or "email" not in user:
        raise BadGateway("User service response has an invalid schema")

    return user
