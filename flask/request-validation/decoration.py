import json
from functools import wraps
from inspect import getfullargspec

from flask import abort, current_app, request
from pydantic import BaseModel, TypeAdapter, ValidationError


def validate_function_arg(arg_name, arg_value):
    return TypeAdapter(arg_name).validate_python(arg_value)


def validate_path_parameters(
    path_params: dict, path_model: BaseModel, annotations: dict
) -> dict:
    # For custom path type converters: https://stackoverflow.com/a/32237936/7728410
    if path_params and path_model is None:
        # if not annotations:
        #     # Developer has used @validate but no model and no type hints
        #     # TODO: Might not need to handle this
        #     abort(
        #         500,
        #         "Must either provide a path_model or use type hints in view function if using url parameters",
        #     )

        validated_args = {}
        for arg, value in path_params.items():
            try:
                validated_args[arg] = validate_function_arg(annotations[arg], value)
            except ValidationError as e:
                abort(400, e)
            except KeyError as e:
                raise KeyError(f"{e}. Check the flask route function type hints")
        return validated_args
    # elif not path_params and path_model is not None:
    #     # TODO: Might not need to handle this
    #     abort(500, "Path model provided but no url parameters in path")
    return as_model(path_params, path_model)


def validate_path_parameters_from_type_hints(
    path_params: dict, annotations: dict
) -> dict:
    # For custom path type converters: https://stackoverflow.com/a/32237936/7728410
    if not annotations:
        # Because we want an error only if no type annotations and no path_model
        raise TypeError(f"Untyped path parameters: {list(path_params.keys())}")

    valid_view_args = {}
    for arg, value in path_params.items():
        try:
            result = TypeAdapter(annotations[arg]).validate_python(value)
        except ValidationError as e:
            abort(400, e)
        valid_view_args[arg] = result
    return valid_view_args


def validate_query_parameters(query_params, query_model):
    # Query params sent but query is None: End user might have just sent query params -> DO NOTHING
    # Query params not sent, but query not None: End user just didn't send query params -> DO NOTHING
    return as_model(query_params, query_model)


def validate_body(body, body_model):
    if body and body_model is None:
        # End user sent a body but dev didn't expect one
        abort(400, "Bad request")
    return as_model(body, body_model)


def as_model(data: dict, model: BaseModel) -> dict:
    if model is not None:
        try:
            return model(**data).model_dump()
        except ValidationError as e:
            abort(400, json.loads(e.json()))
    return {}


def has_body(request):
    # RFC7230 - 3.3. Message Body: Presence of body in request is signaled by
    #   a Content-Length or Transfer-Encoding header field.
    return "Transfer-Encoding" in request.headers or "Content-Length" in request.headers


def validate(body: BaseModel = None, query: BaseModel = None, path: BaseModel = None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not any([body, query, path]):
                current_app.logger.debug(
                    "Validate decorator was used but no validation model was provided."
                )

            # Validate the path parameters
            spec = getfullargspec(f)  # Get args & type hints from the route function

            # if request.view_args and path is None:
            #     # Args were provided to the path, but no path model was specified
            #     request.path_params = validate_path_parameters_from_type_hints(
            #         request.view_args, spec.annotations
            #     )
            # else:
            request.path_params = validate_path_parameters(
                request.view_args, path, spec.annotations
            )

            # Validate the query parameters
            request.query_params = validate_query_parameters(
                request.args.to_dict(), query
            )

            # Validate the request body
            request.body = {}
            if has_body(request):
                request.body = validate_body(request.get_json(), body)
            return f(*args, **kwargs)

        return wrapper

    return decorator
