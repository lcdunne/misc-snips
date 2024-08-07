import uuid
from datetime import datetime, timezone
from typing import Callable, Generic, TypeVar

from flask import Flask, Response
from pydantic import BaseModel, Field, field_serializer

DataT = TypeVar("DataT")


def get_now(fmt: str = "%Y-%m-%dT%H:%M:%S") -> str:
    return datetime.now(timezone.utc).strftime(fmt)


class CustomResponse(Response):
    # Change the default response type to JSON
    default_mimetype = "application/json"


class CustomResponseModel(BaseModel, Generic[DataT]):
    timestamp: datetime = Field(default_factory=get_now)
    status: int = 200  # Could be more specific
    status_message: str | None = Field(default="OK", alias="statusMessage")
    data: DataT | None = None

    def dump(self, *args, **kwargs):
        """Custom model dump."""
        return self.model_dump(mode="json", *args, **kwargs)


class Category(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    fun: Callable = lambda x: print(x)

    @field_serializer("fun")
    def serialize_fun(self, fun: Callable):
        return f"{fun.__name__}" if hasattr(fun, "__name__") else "lambda"


class UserData(BaseModel):
    id: int
    name: str
    email: str
    category: Category


app = Flask(__name__)
app.response_class = CustomResponse


@app.route("/")
def index():
    # Old approach doesn't break
    return {"status": "ok"}


@app.route("/user")
def user():
    category = Category()
    user_data = UserData(id=1, name="Bob", email="bob@example.com", category=category)
    return CustomResponseModel[UserData](data=user_data, status=201).dump(), 201


@app.route("/users")
def users():
    users_data = [
        UserData(id=1, name="John Doe", email="john@example.com", category=Category()),
        UserData(id=2, name="Jane Doe", email="jane@example.com", category=Category()),
    ]
    return CustomResponseModel[list[UserData]](data=users_data).dump()


if __name__ == "__main__":
    app.run()
