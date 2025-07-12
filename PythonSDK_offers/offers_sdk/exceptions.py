import httpx


class OffersAPIError(Exception):
    """Base exception for Offers API errors."""

    def __init__(self, response: httpx.Response):
        self.status_code = response.status_code
        self.response = response
        try:
            self.detail = response.json().get("detail", response.text)
            
        except Exception:
            self.detail = response.text

        super().__init__(self._format_message())

    def _format_message(self) -> str:
        return f"[{self.status_code}] Offers API Error: {self.detail}"


class AuthenticationError(OffersAPIError):
    '''Error code 401, bad authentication.'''
    def __init__(self, response: httpx.Response):
        super().__init__(response)


class ProductNotFoundError(OffersAPIError):
    '''Error code 404, not registred product.'''
    def __init__(self, response: httpx.Response):
        super().__init__(response)


class ProductDuplicityError(OffersAPIError):
    '''Error code 409, product already registred.'''
    def __init__(self, response: httpx.Response):
        super().__init__(response)


class BadRequestError(OffersAPIError):
    '''Error code 400/422, bad request.'''
    def __init__(self, response: httpx.Response):
        super().__init__(response)

class ValidationError(OffersAPIError):
    '''Error code 422, validation error.'''
    def __init__(self, response: httpx.Response):
        super().__init__(response)
