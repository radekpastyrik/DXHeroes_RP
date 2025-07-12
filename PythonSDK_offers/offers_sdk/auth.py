from .exceptions import *  # import of all exceptions + httpx
# import httpx
import json
from typing import Optional
from pathlib import Path
from datetime import datetime, timedelta

TOKEN_CACHE_FILE = Path(".auth_token_cache.json")
TOKEN_VALIDITY_SECONDS = 5 * 60  # 5 minutes expiration time


class AuthManager:
    '''
    AuthManager is created with purpose of checking given refresh token which will be used to create an active access token.

    Access token is active for a five minutes.
    Automatically solves the problem with already generated token which is still active via token caching.
    '''
    def __init__(self, auth_url: str, refresh_token: str):
        self._refresh_token = refresh_token
        self._auth_url = auth_url
        self._access_token: Optional[str] = None

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
        '''Refreshes access token while expired.'''
        headers = {
            "accept": "application/json",
            "Bearer": self._refresh_token
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self._auth_url, headers=headers)
            # Information about provided token and status
            # print("RESPONSE STATUS:", response.status_code)
            # print("RESPONSE BODY:", response.text)

            # Error handling
            error_map = {
                400: BadRequestError,
                401: AuthenticationError,
                422: ValidationError,
            }
            if response.status_code == 201:
                self._access_token = response.json()["access_token"]
                self._save_token_cache(self._access_token)
            else:
                exception_class = error_map.get(response.status_code, OffersAPIError)
                raise exception_class(response)

    def _load_token_cache(self) -> Optional[dict]:
        '''Checker for loading of access token if generated recently.'''
        if not TOKEN_CACHE_FILE.exists():
            return None

        try:
            with open(TOKEN_CACHE_FILE, "r") as f:
                data = json.load(f)
            created_at = datetime.fromisoformat(data["created"])
            if datetime.now() - created_at < timedelta(seconds=TOKEN_VALIDITY_SECONDS):
                return data
            
        except Exception:
            pass  # corrupted or expired, generate a new one

        return None

    def _save_token_cache(self, token: str):
        '''Stores access token in project folder'''
        with open(TOKEN_CACHE_FILE, "w") as f:
            json.dump({
                "access_token": token,
                "created": datetime.now().isoformat()
            }, f)

        # Easiest setting of file: hiding of file - could be extended - crypting, APPDATA,..

            
