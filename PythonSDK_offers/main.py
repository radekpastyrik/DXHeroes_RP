import asyncio
import os
from dotenv import load_dotenv
from offers_sdk.client import OffersClient, Product, Offer, List, UUID, uuid4
from offers_sdk.auth import AuthManager

load_dotenv()
refresh_token: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]

async def main():
    client = OffersClient(base_url=BASE_URL, refresh_token=refresh_token)

    randomUUID: UUID = uuid4()  # possible to use as an argument to register product, not used - automatically generated UUID
    product: Product = await client.register_product(
        # id=randomUUID,
        name="Virtual product",
        description="Some virtual product description."
    )
    print("Registered product:", product)


    offers: List[Offer] = await client.get_offers(product_id=product.id)
    print(f"Offers for product UUID: '{product.id}'\n" + "\n".join(str(offer) for offer in offers))

asyncio.run(main())

async def main_try():
    '''Try authenticate yourself with given refresh token in dotenv.'''
    token = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", refresh_token=refresh_token)
    access_token = await token.get_access_token()


# asyncio.run(main_try())
print("Done.")

