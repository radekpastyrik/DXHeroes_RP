import asyncio
from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4
from offers_sdk.http_clients.requests_client import RequestsClient
from offers_sdk.http_clients.httpx_client import HTTPXClient
from offers_sdk.http_clients.aiohttp_client import AioHTTPClient
from offers_sdk.http_clients.retry_client import RetryingHTTPClient

from hooks.hooks import HookManager, log_error, log_request, log_response

from config import REFRESH_TOKEN, BASE_URL


async def main():
    # Original HTTP client (can be HTTPXClient or AioHTTPClient)
    hook_manager = HookManager()
    hook_manager.add_request_hook(log_request)
    hook_manager.add_response_hook(log_response)
    hook_manager.add_error_hook(log_error)
    base_http_client = RequestsClient(hooks=hook_manager)  # hooks could be empty or hooks=None

    # Wrapped client with retry logic (exponential backoff, max 5 attempts)
    retrying_client = RetryingHTTPClient(base_http_client, max_attempts=5)

    # Initialize main OffersClient with retry client
    client = OffersClient(
        base_url=BASE_URL,
        refresh_token=REFRESH_TOKEN,
        http_client=retrying_client,
        hooks_usage=False  # you could enable hooks to see debug
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
