from offers_sdk.http_clients.sync_client import SyncOffersClient
from offers_sdk.models import Product, Offer, UUID, uuid4
from typing import List

from config import REFRESH_TOKEN, BASE_URL

def main():
    products = [
        Product(name="Virtual product A", description="...", id=uuid4()),
        Product(name="Virtual product B", description="...", id=uuid4()),
        Product(name="Virtual product C", description="...", id=uuid4())
    ]

    # Define http client
    http_client_definition = None  # defualt
    # Use synchronous client - defaultly HTTPX client is used
    client = SyncOffersClient(base_url=BASE_URL, 
                              refresh_token=REFRESH_TOKEN, 
                              http_client=http_client_definition,
                              hooks_usage=False)  # you can define hooks usage

    results = client.register_products_batch(products)
    print("Batch registration results:")
    for r in results:
        print(r)

    randomUUID: UUID = uuid4()
    product = client.register_product(
        id=randomUUID,
        name="Virtual product",
        description="Some virtual product description."
    )
    print("\nRegistered product:")
    print(product)

    offers: List[Offer] = client.get_offers(product_id=str(randomUUID))
    print(f"\nOffers for product UUID '{product.id}':")
    for offer in offers:
        print(offer)

    client.close()

if __name__ == "__main__":
    main()
    print("Done.")
