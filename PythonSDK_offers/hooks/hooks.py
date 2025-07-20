from typing import Callable, Awaitable, Any, Literal

RequestHook = Callable[[str, str, dict, dict], Awaitable[None]]  # method, url, headers, payload
ResponseHook = Callable[[str, str, Any], Awaitable[None]]        # method, url, response
ErrorHook = Callable[[str, str, Exception], Awaitable[None]]     # method, url, error


class HookManager:
    def __init__(self, hooks_usage: bool = False):
        self.on_request: list[RequestHook] = []
        self.on_response: list[ResponseHook] = []
        self.on_error: list[ErrorHook] = []
        self.usage: bool = hooks_usage

    def add_request_hook(self, hook: RequestHook, update_option: Literal["add", "replace"] = "add"):
        if update_option.startswith("r"):
            self.on_request = hook
            return
        self.on_request.append(hook)

    def add_response_hook(self, hook: ResponseHook, update_option: Literal["add", "replace"] = "add"):
        if update_option.startswith("r"):
            self.on_response = hook
            return
        self.on_response.append(hook)

    def add_error_hook(self, hook: ErrorHook, update_option: Literal["add", "replace"] = "add"):
        if update_option.startswith("r"):
            self.on_error = hook
            return
        self.on_error.append(hook)

    async def run_request_hooks(self, method: str, url: str, headers: dict, json: dict):
        if not self.usage:
            return
        for hook in self.on_request:
            await hook(method, url, headers, json)

    async def run_response_hooks(self, method: str, url: str, response: Any):
        if not self.usage:
            return
        for hook in self.on_response:
            await hook(method, url, response)

    async def run_error_hooks(self, method: str, url: str, error: Exception):
        if not self.usage:
            return
        for hook in self.on_error:
            await hook(method, url, error)

async def log_request(method, url, headers, payload):
    print(f"1. [REQ] {method} \n2. {url} \n3. headers={headers} \n4. payload={payload}")

async def log_response(method, url, response):
    status = response.status if hasattr(response, "status") else response.status_code
    print(f"1.[RES] {method} \n2. {url} \n3. {status}")

async def log_error(method: str, url: str, error: Exception):
    print(f"1.[ERR] {method} \n2.{url} \n3. {type(error).__name__}: {error}")
