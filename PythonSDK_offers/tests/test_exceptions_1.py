import pytest
from httpx import Response
from offers_sdk.exceptions import (
    OffersAPIError,
    AuthenticationError,
    ProductNotFoundError,
    ProductDuplicityError,
    BadRequestError,
    ValidationError,
)

def make_response(status_code, json_body=None):
    """Helper to create a fake HTTPX response."""
    return Response(
        status_code=status_code,
        json=json_body or {"detail": "Something went wrong"}
    )

@pytest.mark.parametrize("exception_cls,status_code,expected_detail", [
    (AuthenticationError, 401, "Bad auth"),
    (ProductNotFoundError, 404, "Product not found"),
    (ProductDuplicityError, 409, "Product already registered"),
    (BadRequestError, 400, "Bad request"),
    (ValidationError, 422, "Validation failed"),
    (OffersAPIError, 500, "Unexpected error"),
])
def test_exceptions_format(exception_cls, status_code, expected_detail):
    response = make_response(status_code, {"detail": expected_detail})
    error = exception_cls(response)

    # Assert correct status code
    assert error.status_code == status_code

    # Assert detail is correctly extracted
    assert expected_detail in str(error)

    # Assert message is correctly formatted
    assert str(status_code) in str(error)
    assert isinstance(error, OffersAPIError)


def test_fallback_when_no_json():
    """Ensure fallback when response doesn't have valid JSON."""
    class DummyResponse:
        status_code = 418
        def json(self): raise ValueError("nope")

    error = OffersAPIError(DummyResponse())
    assert "[418]" in str(error)
    assert "Offers API Error" in str(error)


def test_fallback_when_json_is_not_dict():
    """Handles case when `response.json()` returns a list or string."""
    class DummyResponse:
        status_code = 418
        def json(self): return ["unexpected"]

    error = OffersAPIError(DummyResponse())
    assert "['unexpected']" in str(error)
