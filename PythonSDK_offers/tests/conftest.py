import pytest
import respx
from httpx import Response

BASE_URL = "https://python.exercise.applifting.cz"
AUTH_URL = f"{BASE_URL}/api/v1/auth"

@pytest.fixture
def refresh_token() -> str:
    return "dummy-refresh-token"

@pytest.fixture
def base_url() -> str:
    return BASE_URL
