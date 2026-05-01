import requests

from services.order_service.order_service import create_app
from services.order_service.order_service import clients as user_client


class DummyResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


def test_create_order_success(monkeypatch):
    app = create_app(testing=True)
    client = app.test_client()

    def fake_get(url, timeout):
        assert url.endswith("/users/1")
        assert timeout > 0
        return DummyResponse(
            200,
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
        )

    monkeypatch.setattr(user_client.requests, "get", fake_get)

    response = client.post(
        "/orders",
        json={"user_id": 1, "item": "Book", "price": 10.5},
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 1
    assert data["user_id"] == 1
    assert data["item"] == "Book"
    assert data["price"] == 10.5
    assert data["user_name"] == "Alice"
    assert data["user_email"] == "alice@example.com"
    assert "created_at" in data


def test_create_order_rejects_invalid_payload():
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post("/orders", json={"user_id": "1", "item": "Book", "price": 10})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "BAD_REQUEST"


def test_create_order_returns_400_when_user_does_not_exist(monkeypatch):
    app = create_app(testing=True)
    client = app.test_client()

    def fake_get(url, timeout):
        return DummyResponse(404, {"error": {"code": "NOT_FOUND"}})

    monkeypatch.setattr(user_client.requests, "get", fake_get)

    response = client.post(
        "/orders",
        json={"user_id": 99, "item": "Book", "price": 10},
    )

    assert response.status_code == 400
    assert "does not exist" in response.get_json()["error"]["message"]


def test_create_order_returns_503_when_user_service_is_down(monkeypatch):
    app = create_app(testing=True)
    client = app.test_client()

    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError("connection refused")

    monkeypatch.setattr(user_client.requests, "get", fake_get)

    response = client.post(
        "/orders",
        json={"user_id": 1, "item": "Book", "price": 10},
    )

    assert response.status_code == 503
    assert response.get_json()["error"]["code"] == "SERVICE_UNAVAILABLE"


def test_get_order_success(monkeypatch):
    app = create_app(testing=True)
    client = app.test_client()

    monkeypatch.setattr(
        user_client.requests,
        "get",
        lambda url, timeout: DummyResponse(
            200,
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
        ),
    )
    client.post("/orders", json={"user_id": 1, "item": "Book", "price": 10})

    response = client.get("/orders/1")

    assert response.status_code == 200
    assert response.get_json()["item"] == "Book"
