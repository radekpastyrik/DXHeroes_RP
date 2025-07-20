from .base import AsyncHTTPClient
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from typing import Dict, Any


class RetryingHTTPClient(AsyncHTTPClient):
    def __init__(self, wrapped: AsyncHTTPClient, max_attempts: int = 5):
        super().__init__(hooks=wrapped.hooks)  # důležité: předat hook manager z obaleného klienta
        self._wrapped = wrapped
        self._retry_decorator = retry(
            retry=retry_if_exception_type(Exception),
            wait=wait_exponential(multiplier=0.2, min=0.5, max=10),
            stop=stop_after_attempt(max_attempts),
            reraise=True
        )

    async def get(self, url: str, headers: Dict[str, str]) -> Any:
        method = "GET"
        await self.hooks.run_request_hooks(method, url, headers, {})
        try:
            resp = await self._retry_decorator(self._wrapped.get)(url, headers)
            await self.hooks.run_response_hooks(method, url, resp)
            return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise

    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> Any:
        method = "POST"
        await self.hooks.run_request_hooks(method, url, headers, json)
        try:
            resp = await self._retry_decorator(self._wrapped.post)(url, headers, json)
            await self.hooks.run_response_hooks(method, url, resp)
            return resp
        except Exception as e:
            await self.hooks.run_error_hooks(method, url, e)
            raise
