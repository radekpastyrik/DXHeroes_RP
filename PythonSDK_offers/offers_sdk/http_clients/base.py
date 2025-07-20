# offers_sdk/http_clients/base.py
from abc import ABC, abstractmethod
from typing import Any, Dict
from hooks import HookManager


class AsyncHTTPClient(ABC):
    def __init__(self, hooks: HookManager | None = None):
        self.hooks: HookManager = hooks or HookManager()

    @abstractmethod
    async def get(self, url: str, headers: Dict[str, str]) -> Any:
        ...

    @abstractmethod
    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> Any:
        ...
