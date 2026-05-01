from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        status = HTTPStatus(error.code or 500)
        return (
            jsonify(
                {
                    "error": {
                        "code": status.name,
                        "message": error.description,
                    }
                }
            ),
            status.value,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        if app.config.get("TESTING"):
            raise error

        return (
            jsonify(
                {
                    "error": {
                        "code": HTTPStatus.INTERNAL_SERVER_ERROR.name,
                        "message": "Internal server error",
                    }
                }
            ),
            HTTPStatus.INTERNAL_SERVER_ERROR.value,
        )
