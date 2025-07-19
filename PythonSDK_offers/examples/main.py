import asyncio
import os
from dotenv import load_dotenv
from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4, HTTPXClient, AioHTTPClient, RequestsClient

load_dotenv()
REFRESH_TOKEN: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]

async def main():
    products = [
    Product(name="Virtual product A", description="...", id=uuid4()),
    Product(name="Virtual product B", description="...", id=uuid4()),
    Product(name="Virtual product C", description="...", id=uuid4())
    ]

    # Register products in batch
    client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
    # or define http client
    # client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN, http_client=HTTPXClient())
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

