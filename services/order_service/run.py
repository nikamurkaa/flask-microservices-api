import os

from services.order_service.order_service import create_app


app = create_app()


if __name__ == "__main__":
    host = os.getenv("HOST", os.getenv("ORDER_SERVICE_HOST", "127.0.0.1"))
    port = int(os.getenv("PORT", os.getenv("ORDER_SERVICE_PORT", "5002")))
    app.run(host=host, port=port, debug=False)
