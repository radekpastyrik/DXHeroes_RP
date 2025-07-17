from abc import ABC, abstractmethod
from typing import Any, Dict


class AsyncHTTPClient(ABC):
    @abstractmethod
    async def get(self, url: str, headers: Dict[str, str]) -> Any:
        ...

    @abstractmethod
    async def post(self, url: str, headers: Dict[str, str], json: Dict) -> Any:
        ...
