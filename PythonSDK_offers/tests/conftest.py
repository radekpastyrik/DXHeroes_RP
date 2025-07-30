import pytest
from config import BASE_URL, REFRESH_TOKEN, TOKEN_CACHE_PATH


@pytest.fixture
def refresh_token() -> str:
    return "dummy-refresh-token"

@pytest.fixture
def base_url() -> str:
    return BASE_URL

@pytest.fixture
def valid_refresh_token() -> str:
    return REFRESH_TOKEN

@pytest.fixture
def temp_token_file(tmp_path):
    return tmp_path / TOKEN_CACHE_PATH