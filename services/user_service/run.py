import os

from services.user_service.user_service import create_app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("HOST", os.getenv("USER_SERVICE_HOST", "127.0.0.1"))
    port = int(os.getenv("PORT", os.getenv("USER_SERVICE_PORT", "5001")))
    app.run(host=host, port=port, debug=False)
