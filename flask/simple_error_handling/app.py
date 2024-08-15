from flask import Flask, abort
from werkzeug.exceptions import HTTPException

from error_handlers import handle_exception_as_json, handle_http_exception_as_json

app = Flask(__name__)


@app.after_request
def add_custom_header(response):
    response.headers["X-Custom-Header"] = "Value"
    return response


@app.get("/")
def index():
    return {"message": "OK"}


# @app.get("/widgets")
# def get_widgets():
#     widgets = service.get_widgets()
#     widgets_response = ApiResponse[list[Widget]](widgets, 1000).model_dump()
#     return Response(widgets_response, status=200)


@app.get("/errors/<int:code>")
def err(code):
    abort(code)


@app.get("/exception")
def exc():
    raise Exception("AAA")


app.register_error_handler(Exception, handle_exception_as_json)
app.register_error_handler(HTTPException, handle_http_exception_as_json)


if __name__ == "__main__":
    app.run(debug=True)
