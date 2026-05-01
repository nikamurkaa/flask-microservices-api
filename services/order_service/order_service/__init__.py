from flask import Flask

from .errors import register_error_handlers
from .routes import orders_bp
from .storage import reset_order_store


def create_app(*, testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config.update(TESTING=testing)

    if testing:
        reset_order_store()

    app.register_blueprint(orders_bp)
    register_error_handlers(app)
    return app
