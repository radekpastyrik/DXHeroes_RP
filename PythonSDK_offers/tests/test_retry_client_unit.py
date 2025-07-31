import pytest
from unittest.mock import AsyncMock
from offers_sdk.http_clients.retry_client import RetryingHTTPClient

# Unit test


class DummyFailingClient:
    """Client which fails every time"""
    def __init__(self):
        self.call_count_get = 0
        self.call_count_post = 0
        self.hooks = None

    async def get(self, url, headers):
        self.call_count_get += 1
        raise RuntimeError("Simulated GET failure")

    async def post(self, url, headers, json):
        self.call_count_post += 1
        raise RuntimeError("Simulated POST failure")


class DummySucceedingClient:
    """Client which succeeds immediately"""
    def __init__(self):
        self.hooks = None
        
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
async def test_mocking_retry_client_get_success():
    mock_client = AsyncMock()
    mock_client.get.return_value = "GET_OK"

    client = RetryingHTTPClient(mock_client)

    headers = {"x-test": "value"}
    result = await client.get("https://fake-url", headers=headers)

    assert result == "GET_OK"

    mock_client.get.assert_awaited_once()
    args, _ = mock_client.get.await_args

    assert args[0] == "https://fake-url"
    assert args[1] == headers


@pytest.mark.asyncio
async def test_retry_client_post_success():
    """Test that POST succeeds without retry"""
    base = DummySucceedingClient()
    client = RetryingHTTPClient(base)

    result = await client.post("https://fake-url", headers={}, json={})
    assert result == "POST_OK"


@pytest.mark.asyncio
async def test_mocking_retry_client_post_success():
    """Test that POST succeeds without retry"""
    mock_client = AsyncMock()
    mock_client.post.return_value = "POST_OK"

    client = RetryingHTTPClient(mock_client)

    headers = {"Authorization": "Bearer token"}
    json_data = {"key": "value"}

    result = await client.post("https://fake-url", headers=headers, json=json_data)

    assert result == "POST_OK"

    mock_client.post.assert_awaited_once()
    args, kwargs = mock_client.post.await_args

    assert args[0] == "https://fake-url"
    assert args[1] == headers
    assert args[2] == json_data


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


class DummyFailThenSucceedClient:
    """Client which first fails N times, then succeeds"""
    def __init__(self, fail_count_get=2, fail_count_post=2):
        self.call_count_get = 0
        self.call_count_post = 0
        self.fail_count_get = fail_count_get
        self.fail_count_post = fail_count_post
        self.hooks = None

    async def get(self, url, headers):
        self.call_count_get += 1
        if self.call_count_get <= self.fail_count_get:
            raise RuntimeError(f"Simulated GET failure attempt {self.call_count_get}")
        return {"status": "GET_SUCCESS", "attempt": self.call_count_get}

    async def post(self, url, headers, json):
        self.call_count_post += 1
        if self.call_count_post <= self.fail_count_post:
            raise RuntimeError(f"Simulated POST failure attempt {self.call_count_post}")
        return {"status": "POST_SUCCESS", "attempt": self.call_count_post, "data": json}


@pytest.mark.asyncio
async def test_retry_client_get_fails_then_succeeds():
    """Test GET which fails 2x and then succeeds on 3rd attempt"""
    base = DummyFailThenSucceedClient(fail_count_get=2)
    client = RetryingHTTPClient(base, max_attempts=5)

    # Expected success on 3rd attempt
    result = await client.get("https://test-url", headers={"test": "header"})
    
    assert result["status"] == "GET_SUCCESS"
    assert result["attempt"] == 3  # Failed 2x, succeeded on 3rd
    assert base.call_count_get == 3


@pytest.mark.asyncio
async def test_retry_client_post_fails_then_succeeds():
    """Test POST which fails 1x and then succeeds on 2nd attempt"""
    base = DummyFailThenSucceedClient(fail_count_post=1)
    client = RetryingHTTPClient(base, max_attempts=3)

    test_data = {"key": "value", "test": True}
    
    # Expected success on 2nd attempt
    result = await client.post("https://test-url", headers={}, json=test_data)
    
    assert result["status"] == "POST_SUCCESS"
    assert result["attempt"] == 2  # Failed 1x, succeeded on 2nd
    assert result["data"] == test_data
    assert base.call_count_post == 2


@pytest.mark.asyncio
async def test_retry_client_fails_max_attempts_minus_one():
    """Test that client succeeds on last possible attempt"""
    base = DummyFailThenSucceedClient(fail_count_get=3)  # Fails 3x
    client = RetryingHTTPClient(base, max_attempts=4)    # Max 4 attempts
    
    # Expected success on 4th (last) attempt
    result = await client.get("https://edge-case-url", headers={})
    
    assert result["status"] == "GET_SUCCESS"
    assert result["attempt"] == 4
    assert base.call_count_get == 4


@pytest.mark.asyncio 
async def test_retry_client_exceeds_max_attempts():
    """Test that when client fails more than max_attempts, it raises an exception"""
    base = DummyFailThenSucceedClient(fail_count_get=5)  # Fails 5x
    client = RetryingHTTPClient(base, max_attempts=3)    # Max 3 attempts
    
    # Expected failure after 3 attempts
    with pytest.raises(RuntimeError, match="Simulated GET failure attempt 3"):
        await client.get("https://failing-url", headers={})
        
    assert base.call_count_get == 3  # Tried only 3x


@pytest.mark.asyncio
async def test_retry_with_mock_side_effect():
    """Test retry using mock with side_effect - alternative approach"""
    from unittest.mock import AsyncMock
    
    mock_client = AsyncMock()
    
    # Set side_effect: first 2 exceptions, then success
    mock_client.get.side_effect = [
        RuntimeError("Mock failure 1"),
        RuntimeError("Mock failure 2"), 
        {"mock": "success", "attempt": 3}
    ]
    mock_client.hooks = None
    
    client = RetryingHTTPClient(mock_client, max_attempts=4)
    
    result = await client.get("https://mock-url", headers={"auth": "token"})
    
    assert result["mock"] == "success"
    assert result["attempt"] == 3
    assert mock_client.get.call_count == 3  # Called 3x total
