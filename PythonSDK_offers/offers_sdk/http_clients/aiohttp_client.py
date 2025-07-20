# offers_sdk/http_clients/aiohttp_client.py

import aiohttp
from .base import AsyncHTTPClient


class AioHTTPClient(AsyncHTTPClient):
    async def get(self, url: str, headers: dict) -> aiohttp.ClientResponse:
        method = "GET"
        await self.hooks.run_request_hooks(method, url, headers, {})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    resp.json_data = await resp.json()
                    await self.hooks.run_response_hooks(method, url, resp)
                    return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise

    async def post(self, url: str, headers: dict, json: dict) -> aiohttp.ClientResponse:
        method = "POST"
        await self.hooks.run_request_hooks(method, url, headers, json)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=json) as resp:
                    resp.json_data = await resp.json()
                    await self.hooks.run_response_hooks(method, url, resp)
                    return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise
