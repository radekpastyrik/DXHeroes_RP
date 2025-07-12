import pytest
import respx
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer
from uuid import uuid4
from httpx import Response

@pytest.mark.asyncio
@respx.mock
async def test_register_product_success(refresh_token, base_url):
    product_id = str(uuid4())
    # Mocking of request with definition of responses
    respx.post(f"{base_url}/api/v1/auth").mock(
        return_value=Response(201, json={"access_token": "access"})
    )
    respx.post(f"{base_url}/api/v1/products/register").mock(
        return_value=Response(201, json={"id": product_id})
    )

    client = OffersClient(base_url=base_url, refresh_token=refresh_token)

    # Register product with specific name and description
    product = await client.register_product(name="Test", description="Desc")

    # Test instance, name and description of the product
    assert isinstance(product, Product)
    assert str(product.id) == product_id
    assert product.name == "Test"
    assert product.description == "Desc"

@pytest.mark.asyncio
@respx.mock
async def test_get_offers_success(refresh_token, base_url):
    product_id = str(uuid4())
    offers_data = [
        {"id": str(uuid4()), "price": 99, "items_in_stock": 10},
        {"id": str(uuid4()), "price": 199, "items_in_stock": 5}
    ]

    # Mocking of request with definition of responses
    respx.post(f"{base_url}/api/v1/auth").mock(
        return_value=Response(201, json={"access_token": "access"})
    )
    respx.get(f"{base_url}/api/v1/products/{product_id}/offers").mock(
        return_value=Response(200, json=offers_data)
    )

    client = OffersClient(base_url=base_url, refresh_token=refresh_token)
    # Testing of gathering offers function to check number of offers and instances correctness
    offers = await client.get_offers(product_id=product_id)

    # Testing amount of offers for the product and all instances
    assert len(offers) == 2
    assert all(isinstance(offer, Offer) for offer in offers)
