from datetime import datetime

from flask import Blueprint, Flask, abort, request

app = Flask(__name__)

# Blueprints to separate HTML pages from JSON endpoints
view = Blueprint("view", __name__)
api = Blueprint("api", __name__, url_prefix="/api")


# Specific function to return error responses in JSON format
def handle_errors_with_json(error):
    return {
        "error": {
            "error": error.name,
            "detail": error.description,
            "code": error.code,
        },
        "timestamp": datetime.now(),
    }, error.code


# General handler to account for 404 & 405, which are special cases
def handle_errors(error):
    # Logic to check if api is in the path. There are several options:
    #   1. Check if 'api' is in the path - simple but not necessarily ideal
    #   2. ???
    if request.path.startswith("/api"):
        return handle_errors_with_json(error)
    # Or e.g. return render_template(f"{error.code}.html")
    return error, error.code


for code in [404, 405]:
    # Handle these globally
    app.register_error_handler(code, handle_errors)

for code in [400, 401, 403, 415, 500]:
    # Handle these for a specific blueprint
    api.register_error_handler(code, handle_errors_with_json)


@view.route("/<int:error_code>")
def error_page(error_code: int):
    abort(error_code)
    return error_code


@api.route("/<int:error_code>")
def error_json(error_code: int):
    abort(error_code)
    return {"error_code": error_code}


app.register_blueprint(view)
app.register_blueprint(api)

if __name__ == "__main__":
    app.run()
