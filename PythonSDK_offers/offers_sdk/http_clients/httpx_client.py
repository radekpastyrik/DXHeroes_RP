# offers_sdk/http_clients/httpx_client.py
import httpx
from .base import AsyncHTTPClient


class HTTPXClient(AsyncHTTPClient):
    async def get(self, url: str, headers: dict) -> httpx.Response:
        method = "GET"
        await self.hooks.run_request_hooks(method, url, headers, {})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
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
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=json)
                response.json_data = response.json()
            await self.hooks.run_response_hooks(method, url, response)
            return response
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise
