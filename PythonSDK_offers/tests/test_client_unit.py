import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4, UUID
from offers_sdk.client import OffersClient
from offers_sdk.models import Product, Offer
from offers_sdk.exceptions import (
    AuthenticationError, 
    ProductNotFoundError, 
    ProductDuplicityError, 
    BadRequestError,
    OffersAPIError
)


class MockResponse:
    """Mock class for simulating HTTP responses of various clients"""
    def __init__(self, status_code: int, json_data, has_status_attr=True):
        if has_status_attr:
            self.status = status_code  # aiohttp style
        self.status_code = status_code  # requests style
        self.json_data = json_data

    async def json(self):
        return self.json_data


class TestOffersClientInit:
    """Testing initialization of OffersClient"""
    
    def test_init_with_defaults(self, base_url, refresh_token):
        """Testing initialization with default parameters"""
        client = OffersClient(base_url=base_url, refresh_token=refresh_token)
        
        assert client._base_url == base_url
        assert client._auth._refresh_token == refresh_token
        assert client._auth._auth_url == f"{base_url}/api/v1/auth"
        # Default HTTP client should be HTTPXClient
        from offers_sdk.http_clients.httpx_client import HTTPXClient
        assert isinstance(client._http, HTTPXClient)

    def test_init_with_custom_http_client(self, base_url, refresh_token):
        """Testing initialization with custom HTTP client"""
        mock_client = AsyncMock()
        client = OffersClient(
            base_url=base_url, 
            refresh_token=refresh_token, 
            http_client=mock_client
        )
        
        assert client._http is mock_client


class TestOffersClientGetHeaders:
    """Testing _get_headers method"""
    
    @pytest.mark.asyncio
    async def test_get_headers_success(self, base_url, refresh_token):
        """Testing successful getting headers"""
        mock_http_client = AsyncMock()
        client = OffersClient(
            base_url=base_url, 
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        # Mock AuthManager for getting token
        with patch.object(client._auth, 'get_access_token', return_value="test-access-token"):
            headers = await client._get_headers()
            
            expected_headers = {
                "accept": "application/json",
                "Content-Type": "application/json", 
                "Bearer": "test-access-token"
            }
            assert headers == expected_headers


class TestOffersClientRegisterProduct:
    """Testing register_product method"""
    
    @pytest.mark.asyncio
    async def test_register_product_success(self, base_url, refresh_token):
        """Testing successful registration of product"""
        product_id = str(uuid4())
        mock_http_client = AsyncMock()
        
        # Mock HTTP response
        mock_response = MockResponse(201, {"id": product_id})
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        # Mock _get_headers
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            product = await client.register_product(
                name="Test Product", 
                description="Test Description"
            )
            
            # Testing the result
            assert isinstance(product, Product)
            assert str(product.id) == product_id
            assert product.name == "Test Product"
            assert product.description == "Test Description"
            
            # Testing the API call
            mock_http_client.post.assert_called_once()
            call_args = mock_http_client.post.call_args
            assert call_args[0][0] == f"{base_url}/api/v1/products/register"

    @pytest.mark.asyncio
    async def test_register_product_with_custom_id(self, base_url, refresh_token):
        """Testing registration of product with custom ID"""
        custom_id = uuid4()
        mock_http_client = AsyncMock()
        
        mock_response = MockResponse(201, {"id": str(custom_id)})
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            product = await client.register_product(
                name="Test", 
                description="Desc", 
                id=custom_id
            )
            
            assert product.id == custom_id

    @pytest.mark.asyncio
    async def test_register_product_authentication_error(self, base_url, refresh_token):
        """Testing authentication error when registering product"""
        mock_http_client = AsyncMock()
        mock_response = MockResponse(401, {"detail": "Invalid token"})
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(AuthenticationError) as exc_info:
                await client.register_product("Test", "Desc")
            
            assert exc_info.value.status_code == 401
            assert "Invalid token" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_register_product_duplicity_error(self, base_url, refresh_token):
        """Testing product duplicity error when registering product"""
        mock_http_client = AsyncMock()
        mock_response = MockResponse(409, {"detail": "Product already exists"})
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(ProductDuplicityError) as exc_info:
                await client.register_product("Test", "Desc")
            
            assert exc_info.value.status_code == 409

    @pytest.mark.asyncio
    async def test_register_product_validation_error(self, base_url, refresh_token):
        """Testing validation error when registering product"""
        mock_http_client = AsyncMock()
        mock_response = MockResponse(422, {"detail": "Invalid data"})
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(BadRequestError) as exc_info:
                await client.register_product("", "")  # invalid data
            
            assert exc_info.value.status_code == 422


class TestOffersClientGetOffers:
    """Testing get_offers method"""
    
    @pytest.mark.asyncio
    async def test_get_offers_success(self, base_url, refresh_token):
        """Testing successful getting offers"""
        product_id = str(uuid4())
        offers_data = [
            {"id": str(uuid4()), "price": 99, "items_in_stock": 10},
            {"id": str(uuid4()), "price": 199, "items_in_stock": 5}
        ]
        
        mock_http_client = AsyncMock()
        mock_response = MockResponse(200, offers_data)
        mock_http_client.get.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            offers = await client.get_offers(product_id=product_id)
            
            # Testing the result
            assert len(offers) == 2
            assert all(isinstance(offer, Offer) for offer in offers)
            assert offers[0].price == 99
            assert offers[0].items_in_stock == 10
            assert offers[1].price == 199
            assert offers[1].items_in_stock == 5
            
            # Testing the API call
            mock_http_client.get.assert_called_once()
            call_args = mock_http_client.get.call_args
            expected_url = f"{base_url}/api/v1/products/{product_id}/offers"
            assert call_args[0][0] == expected_url


    @pytest.mark.asyncio
    async def test_get_offers_authentication_error(self, base_url, refresh_token):
        """Testing authentication error when getting offers"""
        product_id = str(uuid4())
        
        mock_http_client = AsyncMock()
        mock_response = MockResponse(401, {"detail": "Unauthorized"})
        mock_http_client.get.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(AuthenticationError) as exc_info:
                await client.get_offers(product_id=product_id)
            
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_offers_product_not_found(self, base_url, refresh_token):
        """Testing product not found error when getting offers"""
        product_id = str(uuid4())
        
        mock_http_client = AsyncMock()
        mock_response = MockResponse(404, {"detail": "Product not found"})
        mock_http_client.get.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(ProductNotFoundError) as exc_info:
                await client.get_offers(product_id=product_id)
            
            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_get_offers_validation_error(self, base_url, refresh_token):
        """Testing validation error when getting offers, wrong product_id."""
        invalid_product_id = "invalid-uuid"
        
        mock_http_client = AsyncMock()
        mock_response = MockResponse(422, {"detail": "Invalid UUID format"})
        mock_http_client.get.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            with pytest.raises(BadRequestError) as exc_info:
                await client.get_offers(product_id=invalid_product_id)
            
            assert exc_info.value.status_code == 422


class TestOffersClientResponseHandling:
    """Testing response handling with different HTTP response types"""
    
    @pytest.mark.asyncio
    async def test_response_handling_requests_style(self, base_url, refresh_token):
        """Testing response handling with requests style"""
        mock_http_client = AsyncMock()
        
        # Mock response without 'status' attribute (only 'status_code')
        mock_response = MockResponse(201, {"id": str(uuid4())}, has_status_attr=False)
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            product = await client.register_product("Test", "Desc")
            assert isinstance(product, Product)

    @pytest.mark.asyncio
    async def test_response_handling_json_data_attribute(self, base_url, refresh_token):
        """Testing response handling with json_data attribute (aiohttp style)"""
        mock_http_client = AsyncMock()
        
        # Mock response with json_data attribute
        mock_response = MagicMock()
        mock_response.status = 201
        mock_response.json_data = {"id": str(uuid4())}
        # Remove json() method, so json_data is used
        del mock_response.json
        mock_http_client.post.return_value = mock_response
        
        client = OffersClient(
            base_url=base_url,
            refresh_token=refresh_token,
            http_client=mock_http_client
        )
        
        with patch.object(client, '_get_headers', return_value={"Bearer": "token"}):
            product = await client.register_product("Test", "Desc")
            assert isinstance(product, Product)
