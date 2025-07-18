import pytest
from unittest.mock import AsyncMock
from offers_sdk.http_clients.retry_client import RetryingHTTPClient


class DummyFailingClient:
    """Client which fails every time"""
    def __init__(self):
        self.call_count_get = 0
        self.call_count_post = 0

    async def get(self, url, headers):
        self.call_count_get += 1
        raise RuntimeError("Simulated GET failure")

    async def post(self, url, headers, json):
        self.call_count_post += 1
        raise RuntimeError("Simulated POST failure")


class DummySucceedingClient:
    """Client which succeeds immediately"""
    async def get(self, url, headers):
        return "GET_OK"

    async def post(self, url, headers, json):
        return "POST_OK"


@pytest.mark.asyncio
async def test_retry_client_get_success():
    """Test that GET succeeds without retry"""
    base = DummySucceedingClient()
    client = RetryingHTTPClient(base)

    result = await client.get("https://fake-url", headers={})
    assert result == "GET_OK"

@pytest.mark.asyncio
async def test_retry_client_post_success():
    """Test that POST succeeds without retry"""
    base = DummySucceedingClient()
    client = RetryingHTTPClient(base)

    result = await client.post("https://fake-url", headers={}, json={})
    assert result == "POST_OK"

@pytest.mark.asyncio
async def test_retry_client_get_with_retries():
    """Test that GET retries the correct number of times and then fails"""
    base = DummyFailingClient()
    client = RetryingHTTPClient(base, max_attempts=3)

    with pytest.raises(RuntimeError, match="Simulated GET failure"):
        await client.get("https://fake-url", headers={})

    assert base.call_count_get == 3  # Should try 3x

@pytest.mark.asyncio
async def test_retry_client_post_with_retries():
    """Test that POST retries the correct number of times and then fails"""
    base = DummyFailingClient()
    client = RetryingHTTPClient(base, max_attempts=2)

    with pytest.raises(RuntimeError, match="Simulated POST failure"):
        await client.post("https://fake-url", headers={}, json={})

    assert base.call_count_post == 2
