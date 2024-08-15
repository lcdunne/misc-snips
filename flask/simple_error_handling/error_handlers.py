from flask import current_app
from werkzeug.exceptions import HTTPException, InternalServerError


def get_exception_details(e: Exception) -> tuple[str, str]:
    return type(e).__name__, str(e)


def handle_exception_as_json(e: Exception):
    """Return a 500 HTTP response in case of a general exception."""
    current_app.logger.error(
        "Exception type: %s, details: %s", *get_exception_details(e)
    )
    return {
        "error": "Internal Server Error",
        "message": InternalServerError.description,
        "code": InternalServerError.code,
    }, 500


def handle_http_exception_as_json(e: HTTPException):
    print(type(e))
    return {"error": e.name, "msg": e.description, "code": e.code}, e.code
