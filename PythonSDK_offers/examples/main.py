import asyncio
import os
from dotenv import load_dotenv
from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4, HTTPXClient, AioHTTPClient, RequestsClient
from offers_sdk.auth import AuthManager

load_dotenv()
refresh_token: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]

async def main():
    products = [
    Product(name="Virtual product A", description="...", id=uuid4()),
    Product(name="Virtual product B", description="...", id=uuid4()),
    Product(name="Virtual product C", description="...", id=uuid4())
    ]

    # Register products in batch
    client = OffersClient(base_url=BASE_URL, refresh_token=refresh_token)
    results = await client.register_products_batch(products)
    print(results)


    randomUUID: UUID = uuid4()  # possible to use as an argument to register product, not used - automatically generated UUID
    product: Product = await client.register_product(
        # id=randomUUID,
        name="Virtual product",
        description="Some virtual product description."
    )
    print("Registered product:", product)


    offers: List[Offer] = await client.get_offers(product_id=product.id)
    print(f"Offers for product UUID: '{product.id}'\n" + "\n".join(str(offer) for offer in offers))


if __name__ == "__main__":
    asyncio.run(main())
print("Done.")

