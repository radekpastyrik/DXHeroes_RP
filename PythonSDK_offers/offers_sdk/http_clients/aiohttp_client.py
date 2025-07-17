import aiohttp
from .base import AsyncHTTPClient


class AioHTTPClient(AsyncHTTPClient):
    async def get(self, url: str, headers: dict) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.json_data = await resp.json()
                return resp

    async def post(self, url: str, headers: dict, json: dict) -> aiohttp.ClientResponse:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json) as resp:
                resp.json_data = await resp.json()
                return resp
