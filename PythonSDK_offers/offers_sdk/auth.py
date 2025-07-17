from .http_clients.httpx_client import HTTPXClient
from .http_clients.base import AsyncHTTPClient
from .exceptions import *  # import of all exceptions + httpx
# import httpx
import json
from typing import Optional
from pathlib import Path
from datetime import datetime, timedelta
import asyncio

TOKEN_CACHE_FILE = Path(".auth_token_cache.json")
TOKEN_VALIDITY_SECONDS = 5 * 60  # 5 minutes expiration time


class AuthManager:
    '''
    AuthManager is created with purpose of checking given refresh token which will be used to create an active access token.

    Access token is active for a five minutes.
    Automatically solves the problem with already generated token which is still active via token caching.
    '''
    def __init__(self, auth_url: str, refresh_token: str, http_client: Optional[AsyncHTTPClient] = None, token_cache_path: Optional[Path] = None):
        self._refresh_token = refresh_token
        self._auth_url = auth_url
        self._access_token: Optional[str] = None
        self._client = http_client or HTTPXClient()
        self._token_cache_path = token_cache_path or TOKEN_CACHE_FILE

    def set_token_cache_path(self, path: Path):
        self._token_cache_path = path

    async def get_access_token(self) -> str:
        # Try loading token from cache
        token_data = self._load_token_cache()
        if token_data:
            self._access_token = token_data["access_token"]
            return self._access_token

        # Otherwise fetch new one
        await self.refresh_access_token()
        return self._access_token


    async def refresh_access_token(self):
        headers = {
            "accept": "application/json",
            "Bearer": self._refresh_token
        }

        response = await self._client.post(self._auth_url, headers=headers, json={})
        status = response.status if hasattr(response, "status") else response.status_code
        if hasattr(response, "json_data"):
            body = response.json_data
        else:
            maybe_coro = response.json()
            if asyncio.iscoroutine(maybe_coro):
                body = await maybe_coro
            else:
                body = maybe_coro
        
        error_map = {
            400: BadRequestError,
            401: AuthenticationError,
            422: ValidationError,
        }

        if status == 201:
            self._access_token = body["access_token"]
            self._save_token_cache(self._access_token)
        else:
            detail = body.get("detail", str(body)) if isinstance(body, dict) else str(body)
            exception_class = error_map.get(status, OffersAPIError)
            raise exception_class(status, detail)


    def _load_token_cache(self) -> Optional[dict]:
        '''Checker for loading of access token if generated recently.'''
        if not self._token_cache_path.exists():
            return None

        try:
            with open(self._token_cache_path, "r") as f:
                data = json.load(f)
            created_at = datetime.fromisoformat(data["created"])
            if datetime.now() - created_at < timedelta(seconds=TOKEN_VALIDITY_SECONDS):
                return data
            
        except Exception:
            pass  # corrupted or expired, generate a new one

        return None

    def _save_token_cache(self, token: str):
        '''Stores access token in project folder'''
        with open(self._token_cache_path, "w") as f:
            json.dump({
                "access_token": token,
                "created": datetime.now().isoformat()
            }, f)


            
