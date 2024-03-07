import inspect
from functools import wraps
import asyncio
from typing import Tuple

import aiohttp

from teleapi.core.utils.syntax import default


def as_task(func):
    @wraps(func)
    async def wrapper(*args, **kwargs) -> asyncio.Task:
        return asyncio.create_task(func(*args, **kwargs))

    return wrapper


def wrap_async(func):
    is_coroutine_function = inspect.iscoroutinefunction(func)

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if is_coroutine_function:
            return await func(*args, **kwargs)
        return func(args, **kwargs)

    return wrapper


async def async_http_request(method, url: str, session: dict = None, **kwargs) -> Tuple[aiohttp.ClientResponse, bytes]:
    async with aiohttp.ClientSession(**(default(session, {}))) as s:
        async with s.request(method, url, **kwargs) as response:
            return response, await response.read()
