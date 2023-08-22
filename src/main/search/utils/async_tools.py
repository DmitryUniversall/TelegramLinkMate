import asyncio
from typing import Optional
from functools import partial
from concurrent.futures import Executor


async def run_in_executor(executor: Optional[Executor], function, *args, **kwargs):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, partial(function, *args, **kwargs))
    return result
