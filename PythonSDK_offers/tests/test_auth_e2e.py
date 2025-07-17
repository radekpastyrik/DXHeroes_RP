import os
import pytest
from offers_sdk.auth import AuthManager, TOKEN_CACHE_FILE
from offers_sdk.exceptions import AuthenticationError, BadRequestError, ValidationError, OffersAPIError
from dotenv import load_dotenv
from pathlib import Path
from offers_sdk.http_clients.aiohttp_client import AioHTTPClient
from offers_sdk.http_clients.requests_client import RequestsClient


load_dotenv()
REFRESH_TOKEN: str = os.environ["REFRESH_TOKEN"]
BASE_URL: str = os.environ["BASE_URL"]
# Integration tests

@pytest.mark.asyncio
async def test_auth_manager_e2e_success():
    """E2E: Should get a valid access token using a real refresh token."""
    auth = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", 
                       refresh_token=REFRESH_TOKEN)

    token = await auth.get_access_token()

    assert isinstance(token, str), "Access token must be a string"
    assert len(token) > 10, "Access token seems too short"

@pytest.mark.asyncio
async def test_auth_manager_e2e_bad_request(tmp_path):
    """E2E: Should raise an error for a bad request (400), token already generated."""
    cache_file = tmp_path / "auth_cache.json"
    auth = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", refresh_token=REFRESH_TOKEN, token_cache_path=cache_file)

    with pytest.raises(BadRequestError):
        await auth.refresh_access_token()

@pytest.mark.asyncio
async def test_auth_manager_e2e_invalid_token_httpx(tmp_path):
    """E2E: Should raise an error for an invalid refresh token."""
    invalid_token = "invalid-refresh-token"
    cache_file = tmp_path / "auth_cache.json"
    auth = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", refresh_token=invalid_token, token_cache_path=cache_file)

    with pytest.raises(AuthenticationError):
        await auth.get_access_token()

@pytest.mark.asyncio
async def test_auth_manager_e2e_invalid_token_aiohttp(tmp_path):
    """E2E: Should raise an error for an invalid refresh token."""
    invalid_token = "invalid-refresh-token"
    cache_file = tmp_path / "auth_cache.json"
    auth = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", 
                       refresh_token=invalid_token, 
                       token_cache_path=cache_file,
                       http_client=AioHTTPClient())

    with pytest.raises(AuthenticationError):
        await auth.get_access_token()


@pytest.mark.asyncio
async def test_auth_manager_e2e_invalid_token_http(tmp_path):
    """E2E: Should raise an error for an invalid refresh token."""
    invalid_token = "invalid-refresh-token"
    cache_file = tmp_path / "auth_cache.json"
    auth = AuthManager(auth_url=f"{BASE_URL}/api/v1/auth", 
                       refresh_token=invalid_token, 
                       token_cache_path=cache_file,
                       http_client=RequestsClient())

    with pytest.raises(AuthenticationError):
        await auth.get_access_token()