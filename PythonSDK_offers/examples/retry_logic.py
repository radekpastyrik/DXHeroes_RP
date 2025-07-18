import asyncio
import os
from dotenv import load_dotenv

from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4
from offers_sdk.http_clients.requests_client import RequestsClient
from offers_sdk.http_clients.httpx_client import HTTPXClient
from offers_sdk.http_clients.aiohttp_client import AioHTTPClient
from offers_sdk.http_clients.retry_client import RetryingHTTPClient

load_dotenv()

refresh_token: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]

async def main():
    # Original HTTP client (can be HTTPXClient or AioHTTPClient)
    base_http_client = RequestsClient()

    # Wrapped client with retry logic (exponential backoff, max 5 attempts)
    retrying_client = RetryingHTTPClient(base_http_client, max_attempts=5)

    # Initialize main OffersClient with retry client
    client = OffersClient(
        base_url=BASE_URL,
        refresh_token=refresh_token,
        http_client=retrying_client
    )

    # Register product
    product: Product = await client.register_product(
        name="Virtual product",
        description="Some virtual product description."
    )
    print("Registered product:", product)

    # Get offers for product
    offers: List[Offer] = await client.get_offers(product_id=product.id)
    print(f"\nOffers for product UUID: '{product.id}'")
    for offer in offers:
        print("-", offer)

if __name__ == "__main__":
    asyncio.run(main())
    print("Done.")
