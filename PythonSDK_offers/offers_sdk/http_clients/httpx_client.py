# offers_sdk/http_clients/httpx_client.py
import httpx
from .base import AsyncHTTPClient
from typing import Optional


class HTTPXClient(AsyncHTTPClient):
    def __init__(self, hooks=None, client_config: Optional[dict] = None):
        super().__init__(hooks)
        self._client: Optional[httpx.AsyncClient] = None
        self._client_config = client_config or {}

    async def _ensure_client(self):
        """Ensure client is initialized"""
        if self._client is None:
            self._client = httpx.AsyncClient(**self._client_config)

    async def aclose(self):
        '''Closing instance manually because async with not used in here.'''
        if self._client is not None:
            # Maybe could be used also __aexit__
            await self._client.aclose()

    async def get(self, url: str, headers: dict) -> httpx.Response:
        method = "GET"
        await self.hooks.run_request_hooks(method, url, headers, {})
        try:
            await self._ensure_client()
            response = await self._client.get(url, headers=headers)
            response.json_data = response.json()
            await self.hooks.run_response_hooks(method, url, response)
            return response
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise

    async def post(self, url: str, headers: dict, json: dict) -> httpx.Response:
        method = "POST"
        await self.hooks.run_request_hooks(method, url, headers, json)
        try:
            await self._ensure_client()
            response = await self._client.post(url, headers=headers, json=json)
            response.json_data = response.json()
            await self.hooks.run_response_hooks(method, url, response)
            return response
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise
