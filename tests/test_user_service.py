from services.user_service.user_service import create_app


def test_create_user_success():
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"},
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
    }


def test_get_user_success():
    app = create_app(testing=True)
    client = app.test_client()
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.get_json()["email"] == "alice@example.com"


def test_create_user_rejects_invalid_email():
    app = create_app(testing=True)
    client = app.test_client()

    response = client.post("/users", json={"name": "Alice", "email": "wrong"})

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "BAD_REQUEST"


def test_get_user_returns_404_for_unknown_user():
    app = create_app(testing=True)
    client = app.test_client()

    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"
