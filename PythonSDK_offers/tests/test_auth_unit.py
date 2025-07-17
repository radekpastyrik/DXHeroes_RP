import pytest
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from offers_sdk.auth import AuthManager
from offers_sdk.exceptions import AuthenticationError, BadRequestError, ValidationError, OffersAPIError
from offers_sdk.http_clients.base import AsyncHTTPClient

# Unit test

@pytest.fixture
def temp_token_file(tmp_path):
    return tmp_path / ".auth_token_cache.json"

class MockResponse:
    def __init__(self, status_code: int, json_data: dict):
        self.status_code = status_code
        self._json_data = json_data

    async def json(self) -> dict:
        return self._json_data

@pytest.mark.asyncio
async def test_get_access_token_from_cache(temp_token_file):
    token_data = {
        "access_token": "cached_token",
        "created": (datetime.now() - timedelta(seconds=60)).isoformat()
    }
    temp_token_file.write_text(json.dumps(token_data))  # creates temp file

    auth = AuthManager("https://fake-auth", "refresh_token", token_cache_path=temp_token_file)
    token = await auth.get_access_token()
    assert token == "cached_token"

@pytest.mark.asyncio
async def test_refresh_access_token_success(temp_token_file):
    mock_client = AsyncMock(spec=AsyncHTTPClient)
    mock_response = MockResponse(201, {"access_token": "new_token"})
    mock_client.post.return_value = mock_response

    auth = AuthManager("https://fake-auth", "refresh_token", http_client=mock_client, token_cache_path=temp_token_file)

    token = await auth.get_access_token()
    assert token == "new_token"

    # Check that token was cached
    with open(temp_token_file, "r") as f:
        saved = json.load(f)
    assert saved["access_token"] == "new_token"

@pytest.mark.asyncio
async def test_refresh_token_raises_authentication_error(temp_token_file):
    mock_client = AsyncMock(spec=AsyncHTTPClient)
    mock_response = MockResponse(401, {"detail": "Access token invalid"})
    mock_client.post.return_value = mock_response

    auth = AuthManager("https://fake-auth", "refresh_token", http_client=mock_client, token_cache_path=temp_token_file)

    with pytest.raises(AuthenticationError) as exc_info:
        await auth.refresh_access_token()

    assert "Access token invalid" in str(exc_info.value)
