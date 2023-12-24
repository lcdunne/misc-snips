# Request validation in Flask

Most endpoints that accept data from a client expect a well-defined object. The simple approach in Flask would be to let errors propagate - a user submitting an incorrectly-structured NewUser representation, for example, would result in an error when attempting to create that resource.

Although this works, it does not help the user to understand what they have done wrong and correct their request. To improve on this, we would need to intercept the data in the request and check it against a pre-defined model or schema. Then, we can return meaningful error information so that the user can complete their request.

The purpose of this repo is to show how we can easily accomplish request validation using Pydantic.

#### Notes

This was heavily inspired by `flask-pydantic`; I implement this myself since `flask-pydantic` does not seem to support the latest version of `Pydantic`, and I also am not a fan of even having the option to specify the validation models as Flask's view function arguments. I preferred implementing this myself I was not a fan of specifying query and body arguments in the route function directly, since in Flask this is reserved for path parameters only. Also, I do not think it is necessary to treat form validation as separate from body validation.

#### TODO

- Support list query parameters
