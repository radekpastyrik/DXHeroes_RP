from .base import AsyncHTTPClient
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from typing import Dict, Any
import asyncio

class RetryingHTTPClient(AsyncHTTPClient):
    def __init__(self, wrapped: AsyncHTTPClient, max_attempts: int = 5):
        self._wrapped = wrapped
        self._retry_decorator = retry(
            retry=retry_if_exception_type(Exception),
            wait=wait_exponential(multiplier=0.2, min=0.5, max=10),
            stop=stop_after_attempt(max_attempts),
            reraise=True
        )

    async def get(self, url: str, headers: Dict[str, str]) -> Any:
        return await self._retry_decorator(self._wrapped.get)(url, headers)

    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> Any:
        return await self._retry_decorator(self._wrapped.post)(url, headers, json=json)
