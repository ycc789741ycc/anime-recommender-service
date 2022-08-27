import asyncio
import functools
import logging
from typing import Coroutine
from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger(__name__)


def execute_coroutine_in_event_loop(coroutine: Coroutine):
    """
    This function implement the way to run coroutine in the sync function.
    """
    result = None

    async def coro_wrapper(coroutine: Coroutine):
        nonlocal result
        result = await coroutine

    event_loop = asyncio.get_event_loop()
    if event_loop.is_running():
        with ThreadPoolExecutor(max_workers=1) as executor:
            exec_func = functools.partial(asyncio.run, coro_wrapper(coroutine))
            event_loop.run_in_executor(executor=executor, func=exec_func)

        return result
    else:
        result = event_loop.run_until_complete(
            coroutine
        )

        return result
