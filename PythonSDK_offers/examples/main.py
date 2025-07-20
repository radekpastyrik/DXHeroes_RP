import asyncio
import os
from dotenv import load_dotenv
from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4, HTTPXClient, AioHTTPClient, RequestsClient
from hooks.hooks import HookManager, log_error, log_request, log_response
load_dotenv()
REFRESH_TOKEN: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]


'''
# Example patterns for hooks

async def log_request(method, url, headers, payload):
    print(f"1. [REQ] {method} \n2. {url} \n3. headers={headers} \n4. payload={payload}")


async def log_response(method, url, response):
    status = response.status if hasattr(response, "status") else response.status_code
    print(f"1.[RES] {method} \n2. {url} \n3. {status}")


async def log_error(method: str, url: str, error: Exception):
    print(f"1.[ERR] {method} \n2.{url} \n3. {type(error).__name__}: {error}")'''


async def main():
    '''
    # Example addition of hooks
     
    hook_manager = HookManager()
    hook_manager.add_request_hook(log_request)
    hook_manager.add_response_hook(log_response)
    hook_manager.add_error_hook(log_error)
    http_client = HTTPXClient(hooks=hook_manager)'''

    products = [
    Product(name="Virtual product A", description="...", id=uuid4()),
    Product(name="Virtual product B", description="...", id=uuid4()),
    Product(name="Virtual product C", description="...", id=uuid4())
    ]

    # Register products in batch
    client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN, hooks_usage=True)
    # or define http client
    # client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN, http_client=HTTPXClient())  # or http_client
    results = await client.register_products_batch(products)
    print("Multiple registred products:\n" + "\n".join(str(result) for result in results) + "\n")

    # Register a new single product with defined UUID
    randomUUID: UUID = uuid4()  # possible to use as an argument to register product, not used - automatically generated UUID
    product: Product = await client.register_product(
        id=randomUUID,  # could be empty, then it will be generated automatically
        name="Virtual product",
        description="Some virtual product description."
    )
    print("Registered product:", product)

    # Find offers for a specific product
    offers: List[Offer] = await client.get_offers(product_id=str(randomUUID))
    print(f"Offers for product UUID: '{product.id}'\n" + "\n".join(str(offer) for offer in offers))


if __name__ == "__main__":
    asyncio.run(main())
print("Done.")

