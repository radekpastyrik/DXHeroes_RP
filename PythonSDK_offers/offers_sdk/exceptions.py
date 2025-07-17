class OffersAPIError(Exception):
    """Base exception for Offers API errors."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return f"[{self.status_code}] Offers API Error: {self.detail}"


class AuthenticationError(OffersAPIError):
    """Error code 401, bad authentication."""
    pass


class ProductNotFoundError(OffersAPIError):
    """Error code 404, product not registered."""
    pass


class ProductDuplicityError(OffersAPIError):
    """Error code 409, product already registered."""
    pass


class BadRequestError(OffersAPIError):
    """Error code 400/422, bad request."""
    pass


class ValidationError(OffersAPIError):
    """Error code 422, validation error."""
    pass
