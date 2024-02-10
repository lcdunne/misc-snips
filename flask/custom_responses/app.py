from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from flask import Flask, Response
from datetime import datetime, timezone
from typing import Generic, TypeVar

DataT = TypeVar("DataT")


def get_now(fmt: str = "%Y-%m-%dT%H:%M:%S") -> str:
    return datetime.now(timezone.utc).strftime(fmt)


class CustomFlask(Flask):
    # The recommended approach.
    # See https://github.com/pallets/flask/issues/2736#issuecomment-385037987
    def make_response(self, rv):
        if isinstance(rv, BaseModel):
            rv = rv.dict(), getattr(rv, "status", None)
        elif isinstance(rv, tuple) and isinstance(rv[0], BaseModel):
            model = rv[0].dict()
            if not isinstance(rv[1], (str, int)) and len(rv) == 2:
                rv = (model, model.get("status"), rv[1])
            rv = (model, *rv[1:])
        return super().make_response(rv)


class CustomResponse(Response):
    default_mimetype = "application/json"


class CustomResponseModel(GenericModel, Generic[DataT]):
    timestamp: datetime = Field(default_factory=get_now)
    status: int = 200  # Could be more specific
    status_message: str = Field("OK", alias="statusMessage")
    data: DataT | None = None


class UserData(BaseModel):
    id: int
    name: str
    email: str


app = CustomFlask(__name__)
app.response_class = CustomResponse


@app.route("/")
def index():
    # Old approach doesn't break
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
