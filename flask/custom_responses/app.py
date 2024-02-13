from datetime import datetime, timezone
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

from flask import Flask, Response

DataT = TypeVar("DataT")


def get_now(fmt: str = "%Y-%m-%dT%H:%M:%S") -> str:
    return datetime.now(timezone.utc).strftime(fmt)


class CustomResponse(Response):
    # Change the default response type to JSON
    default_mimetype = "application/json"


class CustomResponseModel(BaseModel, Generic[DataT]):
    timestamp: datetime = Field(default_factory=get_now)
    status: int = 200  # Could be more specific
    status_message: str = Field("OK", alias="statusMessage")
    data: DataT | None = None


class UserData(BaseModel):
    id: int
    name: str
    email: str


app = Flask(__name__)
app.response_class = CustomResponse


@app.route("/")
def index():
    # Old approach doesn't break
    return {"status": "ok"}


@app.route("/user")
def user():
    user_data = UserData(id=1, name="Bob", email="bob@example.com")
    return CustomResponseModel[UserData](data=user_data, status=201).model_dump(), 201


@app.route("/users")
def users():
    users_data = [
        UserData(id=1, name="John Doe", email="john@example.com"),
        UserData(id=2, name="Jane Doe", email="jane@example.com"),
    ]
    return CustomResponseModel[list[UserData]](data=users_data).model_dump()


if __name__ == "__main__":
    app.run()
