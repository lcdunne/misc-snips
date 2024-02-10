# Custom Responses

Pydantic is useful if we want to be very specific about our data definitions, but it can be hard to streamline its use for server responses. This repository shows how we can inherit from the Flask object and override its `make_response` function to support the returning of a `Pydantic` model. The end result is that we can write our routes like so:

```python
@app.route("/user")
def user():
    user_data = UserData(id=1, name="Bob", email="bob@example.com")
    return CustomResponseModel[UserData](data=user_data, status=201)
```

If there is a `"status"` field present, then this becomes the response. If a separate status code is returned as the second element of a `tuple` return type, then that takes precedence. Otherwise, all defaults remain.