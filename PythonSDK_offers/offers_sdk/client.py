from .exceptions import *  # import of all exceptions + httpx
# import httpx
from .auth import AuthManager
from .models import Product, Offer, UUID, uuid4
from typing import List, Optional


class OffersClient:
    def __init__(self, base_url: str, refresh_token: str):
        self._auth = AuthManager(auth_url=f"{base_url}/api/v1/auth", refresh_token=refresh_token)
        self._base_url = base_url

    async def _get_headers(self) -> dict:
        access_token = await self._auth.get_access_token()
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Bearer": access_token
        }
    
    async def register_product(self, name: str, description: str, id: Optional[UUID] = None) -> Product:
        product = Product(
            id=id or uuid4(),  # generates uuid automatically if not inserted
            name=name,
            description=description
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/api/v1/products/register",
                headers=await self._get_headers(),
                json=product.model_dump(mode="json")
            )

            # Error handling
            error_map = {
                401: AuthenticationError,
                409: ProductDuplicityError,
                422: BadRequestError,
            }

            if response.status_code != 201:
                exception_class = error_map.get(response.status_code, OffersAPIError)
                raise exception_class(response)
        
            response_data = response.json()
            return Product(
                id=UUID(response_data["id"]),
                name=name,
                description=description)

    async def get_offers(self, product_id: str) -> List[Offer]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/api/v1/products/{product_id}/offers",
                headers=await self._get_headers()
            )
            
            # Error handling
            error_map = {
                401: AuthenticationError,
                404: ProductNotFoundError,
                422: BadRequestError,
            }

            if response.status_code != 200:
                exception_class = error_map.get(response.status_code, OffersAPIError)
                raise exception_class(response)
            
            return [Offer(**item) for item in response.json()]
