from .exceptions import *  # import of all exceptions + httpx
# import httpx
from .http_clients.base import AsyncHTTPClient
from .http_clients.httpx_client import HTTPXClient  # default backend
from .http_clients.aiohttp_client import AioHTTPClient
from .http_clients.requests_client import RequestsClient
from .auth import AuthManager
from .models import Product, Offer, UUID, uuid4
from typing import List, Optional, Union
import asyncio

class OffersClient:
    def __init__(self, base_url: str, refresh_token: str, http_client: Optional[AsyncHTTPClient] = None):
        self._auth = AuthManager(auth_url=f"{base_url}/api/v1/auth", refresh_token=refresh_token)
        self._base_url = base_url
        self._http = http_client or HTTPXClient()  # defaultly using httpx

    async def _get_headers(self) -> dict:
        access_token = await self._auth.get_access_token()
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Bearer": access_token
        }
    
    async def register_products_batch(self, products: List[Product]) -> List[Union[Product, OffersAPIError]]:
        """Batch implementation using either sequential or parallel calls"""

        async def try_register(p: Product):
            try:
                return await self.register_product(name=p.name, description=p.description, id=p.id)
            except OffersAPIError as e:
                return e

        return await asyncio.gather(*(try_register(p) for p in products))
    

    async def register_product(self, name: str, description: str, id: Optional[UUID] = None) -> Product:
        product = Product(id=id or uuid4(), name=name, description=description)  # generates ID automatically if not provided
        headers = await self._get_headers()
        response = await self._http.post(
            f"{self._base_url}/api/v1/products/register",
            headers=headers,
            json=product.model_dump(mode="json")
        )

        status = response.status if hasattr(response, "status") else response.status_code
        if hasattr(response, "json_data"):
            body = response.json_data
        else:
            maybe_coro = response.json()
            if asyncio.iscoroutine(maybe_coro):
                body = await maybe_coro
            else:
                body = maybe_coro

        error_map = {
            401: AuthenticationError,
            409: ProductDuplicityError,
            422: BadRequestError,
        }

        if status != 201:
            detail = body.get("detail", str(body)) if isinstance(body, dict) else str(body)
            exception_class = error_map.get(status, OffersAPIError)
            raise exception_class(status, detail)

        return Product(id=UUID(body["id"]), name=name, description=description)


    async def get_offers(self, product_id: str) -> List[Offer]:
        headers = await self._get_headers()
        response = await self._http.get(
            f"{self._base_url}/api/v1/products/{product_id}/offers",
            headers=headers
        )

        status = response.status if hasattr(response, "status") else response.status_code
        if hasattr(response, "json_data"):
            body = response.json_data
        else:
            maybe_coro = response.json()
            if asyncio.iscoroutine(maybe_coro):
                body = await maybe_coro
            else:
                body = maybe_coro

        error_map = {
            401: AuthenticationError,
            404: ProductNotFoundError,
            422: BadRequestError,
        }
        if status != 200:
            detail = body.get("detail", str(body)) if isinstance(body, dict) else str(body)
            exception_class = error_map.get(status, OffersAPIError)
            raise exception_class(status, detail)

        return [Offer(**item) for item in body]
