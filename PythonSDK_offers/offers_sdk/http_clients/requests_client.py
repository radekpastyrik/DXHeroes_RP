import requests
import asyncio
from typing import Dict, Any
from .base import AsyncHTTPClient


class RequestsClient(AsyncHTTPClient):
    async def get(self, url: str, headers: Dict[str, str]) -> requests.Response:
        # Command asyncio.to_thread allows to run sync code in separate thread
        return await asyncio.to_thread(requests.get, url, headers=headers)

    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> requests.Response:
        # Command asyncio.to_thread allows to run sync code in separate thread
        return await asyncio.to_thread(requests.post, url, headers=headers, json=json)
