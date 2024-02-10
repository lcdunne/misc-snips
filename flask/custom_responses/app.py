from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from flask import Flask, Response
from datetime import datetime
from typing import Generic, TypeVar

# Define a generic type variable for data
DataT = TypeVar("DataT")


class CustomFlask(Flask):
    def make_response(self, rv):
        # Override this to avoid always calling .json or .dict on the model, and to extract status
        # Convert any Pydantic model to JSON response
        if isinstance(rv, BaseModel):
            rv = rv.dict(), getattr(rv, "status", None)
        elif isinstance(rv, tuple) and isinstance(rv[0], BaseModel):
            model = rv[0].dict()
            if not isinstance(rv[1], (str, int)) and len(rv) == 2:
                # If a tuple of (response, header) was given, extract the status from response
                #   otherwise just use what was given
                rv = (model, model.get("status"), rv[1])
            rv = (model, *rv[1:])
        return super().make_response(rv)


class CustomResponse(Response):
    # Set the default response to be JSON instead of text/html
    default_mimetype = "application/json"


class CustomResponseModel(GenericModel, Generic[DataT]):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: int = 200  # Could be more specific
    status_message: str = "OK"
    data: DataT | None = None


# Example Pydantic model
class UserData(BaseModel):
    id: int
    name: str
    email: str


app = CustomFlask(__name__)
app.response_class = CustomResponse


@app.route("/")
def index():
    return {"status": "ok"}


@app.route("/user")
def user():
    user_data = UserData(id=1, name="Bob", email="bob@example.com")
    return CustomResponseModel[UserData](data=user_data, status=201)


@app.route("/users")
def users():
    users_data = [
        UserData(id=1, name="John Doe", email="john@example.com"),
        UserData(id=2, name="Jane Doe", email="jane@example.com"),
    ]
    return CustomResponseModel[list[UserData]](data=users_data)


if __name__ == "__main__":
    app.run()
