import logging
import inspect
from typing import Any, Optional
from functools import wraps


def log_async_methods(logger_name: Optional[str] = None, log_result: bool = False, log_level: int = logging.DEBUG):  # TODO: Docs
    def decorator(cls):
        def get_wrapper(func):
            logger = logging.getLogger(logger_name if logger_name is not None else f"async_calls.{cls.__module__}.{cls.__name__}")

            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                logger.log(log_level, f"Called method {func.__name__} of class {cls.__name__}")

                result = await func(*args, **kwargs)

                if log_result:
                    logger.log(log_level, f"Got result form method {func.__name__} of class {cls.__name__}: {result}")

                return result

            return wrapper

        for attr in dir(cls):
            if attr.startswith("__"):
                continue

            value = getattr(cls, attr)

            if inspect.iscoroutinefunction(value):
                setattr(cls, attr, get_wrapper(value))

        return cls

    return decorator
