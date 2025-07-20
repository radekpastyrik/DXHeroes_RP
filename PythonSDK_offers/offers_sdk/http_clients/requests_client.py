# offers_sdk/http_clients/requests_client.py

import requests
import asyncio
from typing import Dict
from .base import AsyncHTTPClient


class RequestsClient(AsyncHTTPClient):
    async def get(self, url: str, headers: Dict[str, str]) -> requests.Response:
        method = "GET"
        await self.hooks.run_request_hooks(method, url, headers, {})

        try:
            # Command asyncio.to_thread allows to run sync code in separate thread
            resp = await asyncio.to_thread(requests.get, url, headers=headers)
            await self.hooks.run_response_hooks(method, url, resp)
            return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise

    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> requests.Response:
        method = "POST"
        await self.hooks.run_request_hooks(method, url, headers, json)

        try:
            # Command asyncio.to_thread allows to run sync code in separate thread
            resp = await asyncio.to_thread(requests.post, url, headers=headers, json=json)
            await self.hooks.run_response_hooks(method, url, resp)
            return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise
