import inspect
from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING
from teleapi.types.update import Update
from teleapi.core.utils.syntax import default

if TYPE_CHECKING:
    from .manager import BaseErrorManager


class BaseErrorHandler(ABC):
    class Meta:
        pass

    def __init__(self, manager: 'BaseErrorManager', exception_cls: Type[Exception] = None) -> None:
        self.manager = manager
        self.exception_cls = default(exception_cls, getattr(self.Meta, 'exception_cls', None))

        if self.exception_cls is None:
            raise AttributeError("You must define error handler exception_cls as static property in Meta or in __init__ parameters")

    @abstractmethod
    async def handle(self, error: BaseException, update: Update) -> bool:
        ...


class ErrorHandler(BaseErrorHandler, ABC):
    pass


def handler(*, exception_cls: Type[BaseException], **meta_kwargs):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError("You can use this decorator only with coroutine functions")

        meta = type("Meta", (object,), {"exception_cls": exception_cls, **meta_kwargs})
        handler_cls = type(func.__name__, (ErrorHandler,), {
            "handle": func,
            "Meta": meta
        })

        return handler_cls

    return decorator
