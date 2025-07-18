import asyncio
import uuid
import os
import json
from typing import Optional
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from python_exercise_client.client import Client, AuthenticatedClient
from python_exercise_client.api.default import auth_api_v1_auth_post
from python_exercise_client.api.default import (
    get_offers_api_v1_products_product_id_offers_get,
    register_product_api_v1_products_register_post,
)
from python_exercise_client.models import RegisterProductRequest, AuthResponse

load_dotenv()
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
BASE_URL = os.environ["BASE_URL"]
TOKEN_CACHE_PATH = Path(".auth_token_cache.json")
TOKEN_VALIDITY_SECONDS = 5 * 60  # token valid 5 min
MAIN_DIR = Path(__file__).parent.parent

def load_cached_token() -> Optional[dict]:
    '''Checker for loading of access token if generated recently.'''
    if not (MAIN_DIR / TOKEN_CACHE_PATH).exists():
        return None

    try:
        with open(MAIN_DIR / TOKEN_CACHE_PATH, "r") as f:
            data = json.load(f)
        created_at = datetime.fromisoformat(data["created"])
        if datetime.now() - created_at < timedelta(seconds=TOKEN_VALIDITY_SECONDS):
            return data
        
    except Exception:
        pass  # corrupted or expired, generate a new one

    return None

def save_token(token: str):
    '''Stores access token in project folder'''
    with open(MAIN_DIR / TOKEN_CACHE_PATH, "w") as f:
        json.dump({
            "access_token": token,
            "created": datetime.now().isoformat()
        }, f)

async def get_or_refresh_token(client: Client) -> str | None:
    token = load_cached_token()
    if token:
        print("Loaded token from cache.")
        return token["access_token"]

    print("Requesting new token...")
    auth_response = await auth_api_v1_auth_post.asyncio(
        client=client,
        bearer=REFRESH_TOKEN
    )

    if not auth_response or not isinstance(auth_response, AuthResponse):
        print("Authentication failed!")
        return None

    save_token(auth_response.access_token)
    print("New token obtained and saved.")
    return auth_response.access_token


async def main():
    client = Client(base_url=BASE_URL)
    token = await get_or_refresh_token(client)

    if not token:
        return

    # Automatically created AuthenticatedClient probably contains error header with Authorization: Bearer...
    # ... so we need to add token explicitly to post requests!!!
    auth_client = AuthenticatedClient(base_url=BASE_URL, token=token)

    # Register product
    product_id = uuid.uuid4()
    product_request = RegisterProductRequest(
        id=product_id,
        name="Virtual product",
        description="Some virtual product description."
    )

    register_response = await register_product_api_v1_products_register_post.asyncio(
        client=auth_client,
        body=product_request,
        bearer=token  # explicitly pass token
    )

    if not register_response:
        print("Product registration failed!")
        return

    print(f"Registered product: {product_request.name}")
    print(f"Product ID: {product_id}")

    # Get offers
    offers = await get_offers_api_v1_products_product_id_offers_get.asyncio(
        client=auth_client,
        product_id=product_id,
        bearer=token  # explicitly pass token
    )

    if offers:
        print(f"\nOffers for product UUID: '{product_id}'")
        for offer in offers:
            print(f"Offer ID: {offer.id}, Price: ${offer.price}, Stock: {offer.items_in_stock}")
    else:
        print("No offers found for this product.")


if __name__ == "__main__":
    asyncio.run(main())
    print("Done.")
