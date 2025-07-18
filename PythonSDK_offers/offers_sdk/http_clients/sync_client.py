import asyncio
from typing import List, Optional, Union
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer, UUID
from offers_sdk.exceptions import OffersAPIError

class SyncOffersClient:
    def __init__(self, base_url: str, refresh_token: str, http_client=None):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        self._client = OffersClient(base_url=base_url, refresh_token=refresh_token, http_client=http_client)

    def register_products_batch(self, products: List[Product]) -> List[Union[Product, OffersAPIError]]:
        return self._loop.run_until_complete(self._client.register_products_batch(products))

    def register_product(self, name: str, description: str, id: Optional[UUID] = None) -> Product:
        return self._loop.run_until_complete(self._client.register_product(name=name, description=description, id=id))

    def get_offers(self, product_id: str) -> List[Offer]:
        return self._loop.run_until_complete(self._client.get_offers(product_id))

    def close(self):
        self._loop.close()
