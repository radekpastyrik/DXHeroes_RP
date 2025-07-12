import pytest
import respx
from unittest.mock import patch
from offers_sdk.auth import AuthManager, AuthenticationError
from httpx import Response

@pytest.mark.asyncio
@respx.mock
async def test_get_access_token_success(refresh_token, base_url):
    expected_token = "dummy-access-token"
    respx.post(f"{base_url}/api/v1/auth").mock(
        return_value=Response(201, json={"access_token": expected_token})
    )

    auth = AuthManager(auth_url=f"{base_url}/api/v1/auth", refresh_token=refresh_token)
    token = await auth.get_access_token()

    assert token == expected_token

@pytest.mark.asyncio
@respx.mock
async def test_get_access_token_error(refresh_token, base_url):
    respx.post(f"{base_url}/api/v1/auth").mock(
        return_value=Response(401, json={"detail": "Invalid token"})
    )

    auth = AuthManager(auth_url=f"{base_url}/api/v1/auth", refresh_token=refresh_token)

    with patch.object(auth, '_load_token_cache', return_value=None):
        with pytest.raises(AuthenticationError) as exc:
            await auth.get_access_token()

    assert exc.value.response.status_code == 401
