import os
import pytest
import time
from uuid import uuid4
from dotenv import load_dotenv
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer
from offers_sdk.exceptions import (
    AuthenticationError, 
    ProductNotFoundError, 
    ProductDuplicityError, 
    BadRequestError
)
from offers_sdk.http_clients.httpx_client import HTTPXClient
from offers_sdk.http_clients.aiohttp_client import AioHTTPClient
from offers_sdk.http_clients.requests_client import RequestsClient


load_dotenv()
REFRESH_TOKEN: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]


class TestOffersClientE2E:
    """End-to-end testing of OffersClient against real API"""

    @pytest.mark.asyncio
    async def test_client_e2e_register_and_get_offers_success(self):
        """Successful registration of product and getting offers"""
        client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
        
        # Creating unique product name
        timestamp = int(time.time())
        product_name = f"Test product {timestamp}"
        product_description = f"Test product created at {timestamp}."
        
        # Testing registration of product
        product = await client.register_product(
            name=product_name,
            description=product_description
        )
        
        # Testing registration
        assert isinstance(product, Product)
        assert product.name == product_name
        assert product.description == product_description
        assert product.id is not None
        
        # Test getting offers for registered product
        offers = await client.get_offers(product_id=str(product.id))
        
        # Testing offers
        assert isinstance(offers, list)
        # API can return empty list or offers - both are OK
        for offer in offers:
            assert isinstance(offer, Offer)
            assert offer.id is not None
            assert isinstance(offer.price, int)
            assert isinstance(offer.items_in_stock, int)

    @pytest.mark.asyncio 
    async def test_client_e2e_with_custom_product_id(self):
        """Testing registration of product with custom ID"""
        client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
        
        custom_id = uuid4()
        
        product = await client.register_product(
            id=custom_id,
            name="Custom ID virtual product",
            description="Product with custom UUID"
        )
        
        assert product.id == custom_id

    @pytest.mark.asyncio
    async def test_client_e2e_register_product_duplicate_error(self):
        """Testing duplicate error when registering product"""
        client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
        
        # Use same ID for both registration attempts
        duplicate_id = uuid4()
        timestamp = int(time.time())
        product_name = f"Duplicate Test {timestamp}"
        
        # First registration - should pass
        first_product = await client.register_product(
            id=duplicate_id,
            name=product_name,
            description="First registration"
        )
        assert first_product.id == duplicate_id
        
        # Second registration with same ID - should fail
        with pytest.raises(ProductDuplicityError) as exc_info:
            await client.register_product(
                id=duplicate_id,
                name=f"Duplicate {product_name}",
                description="Second registration - should fail"
            )
        
        assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_client_e2e_get_offers_nonexistent_product(self):
        """Testing error when getting offers for non-existing product"""
        client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
        
        # Use random UUID
        nonexistent_id = str(uuid4())
        
        with pytest.raises(ProductNotFoundError) as exc_info:
            await client.get_offers(product_id=nonexistent_id)
        
        assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_client_e2e_invalid_product_id_format(self):
        """Testing validation error with invalid UUID format"""
        client = OffersClient(base_url=BASE_URL, refresh_token=REFRESH_TOKEN)
        
        invalid_id = "not-a-valid-uuid"
        
        with pytest.raises(BadRequestError) as exc_info:
            await client.get_offers(product_id=invalid_id)
        
        assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_client_e2e_invalid_authentication(self, tmp_path):
        """Testing authentication error with invalid refresh token"""
        invalid_token = "invalid-token"
        cache_file = tmp_path / "auth_cache.json"
        client = OffersClient(base_url=BASE_URL, refresh_token=invalid_token)
        client._auth.set_token_cache_path(cache_file)
        
        with pytest.raises(AuthenticationError) as exc_info:
            await client.register_product(
                name="Failed virtual product",
                description="This should fail due to invalid token"
            )
        
        assert exc_info.value.status_code == 401


class TestOffersClientE2EHttpClients:
    """E2E testing with different HTTP clients"""
    
    @pytest.mark.asyncio
    async def test_client_e2e_with_httpx_client(self):
        """Testing HTTPXClient"""
        client = OffersClient(
            base_url=BASE_URL, 
            refresh_token=REFRESH_TOKEN,
            http_client=HTTPXClient()
        )
        
        product = await client.register_product(
            name="Virtual product via HTTPXClient",
            description="Testing with HTTPXClient"
        )
        
        assert isinstance(product, Product)
        
        offers = await client.get_offers(product_id=str(product.id))
        assert isinstance(offers, list)

    @pytest.mark.asyncio
    async def test_client_e2e_with_aiohttp_client(self):
        """Testing AioHTTPClient"""
        client = OffersClient(
            base_url=BASE_URL, 
            refresh_token=REFRESH_TOKEN,
            http_client=AioHTTPClient()
        )
        
        product = await client.register_product(
            name="Virtual product via AioHTTPClient",
            description="Testing with AioHTTPClient"
        )
        
        assert isinstance(product, Product)
        
        offers = await client.get_offers(product_id=str(product.id))
        assert isinstance(offers, list)

    @pytest.mark.asyncio
    async def test_client_e2e_with_requests_client(self):
        """Testing RequestsClient"""
        client = OffersClient(
            base_url=BASE_URL, 
            refresh_token=REFRESH_TOKEN,
            http_client=RequestsClient()
        )
        
        product = await client.register_product(
            name="Virtual product via RequestsClient",
            description="Testing with RequestsClient"
        )
        
        assert isinstance(product, Product)
        
        offers = await client.get_offers(product_id=str(product.id))
        assert isinstance(offers, list)
