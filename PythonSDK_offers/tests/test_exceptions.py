import pytest
from httpx import Response
from offers_sdk.exceptions import AuthenticationError, ProductNotFoundError

def make_response(status_code, json_body):
    return Response(status_code, json=json_body)

def test_authentication_error():
    response = make_response(401, {"detail": "Bad token"})
    err = AuthenticationError(response)
    assert "401" in str(err)

def test_not_found_error():
    response = make_response(404, {"detail": "Not found"})
    err = ProductNotFoundError(response)
    assert "404" in str(err)
