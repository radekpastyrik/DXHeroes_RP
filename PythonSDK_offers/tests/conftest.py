import pytest
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL: str = os.environ["BASE_URL"]
REFRESH_TOKEN: str = os.environ["REFRESH_TOKEN"]

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
    return tmp_path / ".auth_token_cache.json"