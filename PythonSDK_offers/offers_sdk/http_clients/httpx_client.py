# offers_sdk/http_clients/httpx_client.py

import httpx
from .base import AsyncHTTPClient


class HTTPXClient(AsyncHTTPClient):
    async def get(self, url: str, headers: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.get(url, headers=headers)

    async def post(self, url: str, headers: dict, json: dict) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.post(url, headers=headers, json=json)
