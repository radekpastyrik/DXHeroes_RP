import pytest

BASE_URL = "https://python.exercise.applifting.cz"

@pytest.fixture
def refresh_token() -> str:
    return "dummy-refresh-token"

@pytest.fixture
def base_url() -> str:
    return BASE_URL
