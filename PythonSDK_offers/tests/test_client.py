import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer

class MockResponse:
    def __init__(self, status_code: int, json_data):
        self.status = status_code
        self.status_code = status_code
        self.json_data = json_data

    async def json(self):
        return self.json_data

@pytest.mark.asyncio
async def test_register_product_success(refresh_token, base_url):
    product_id = str(uuid4())

    mock_http_client = AsyncMock()
    # Mock odpověď na autentizaci (POST)
    mock_http_client.post.side_effect = [
        MockResponse(201, {"access_token": "access"}),  # auth token
        MockResponse(201, {"id": product_id}),          # registrace produktu
    ]

    client = OffersClient(base_url=base_url, refresh_token=refresh_token)
    client._auth._client = mock_http_client  # správný přístup k http klientovi v auth

    product = await client.register_product(name="Test", description="Desc")

    assert isinstance(product, Product)
    assert str(product.id) == product_id
    assert product.name == "Test"
    assert product.description == "Desc"

'''@pytest.mark.asyncio
async def test_get_offers_success(refresh_token, base_url):
    product_id = str(uuid4())
    offers_data = [
        {"id": str(uuid4()), "price": 99, "items_in_stock": 10},
        {"id": str(uuid4()), "price": 199, "items_in_stock": 5}
    ]

    mock_http_client = AsyncMock()
    # Mock odpověď na autentizaci (POST)
    mock_http_client.post.return_value = MockResponse(201, {"access_token": "access"})
    # Mock odpověď na get offers (GET)
    mock_http_client.get.return_value = MockResponse(200, offers_data)

    client = OffersClient(base_url=base_url, refresh_token=refresh_token)
    client._auth._client = mock_http_client  # správný přístup

    offers = await client.get_offers(product_id=product_id)

    assert len(offers) == 2
    assert all(isinstance(offer, Offer) for offer in offers)'''
