import inspect
import logging
import sys
from abc import abstractmethod
from functools import wraps
from typing import List, Type

from teleapi.core.utils.collections import find_in_list
from teleapi.core.utils.collectors import CollectorMeta, collect_subclasses
from teleapi.core.utils.errors import get_traceback_text
from teleapi.types.update import Update
from .handler import BaseErrorHandler, handler

logger = logging.getLogger(__name__)


class ErrorManagerMeta(CollectorMeta):
    _collector = {
        'func': collect_subclasses,
        'attributes': {
            BaseErrorHandler: '__dynamic_handlers__'
        }
    }


class BaseErrorManager(metaclass=ErrorManagerMeta):
    # Dynamic generated property, that collects handlers(BaseErrorHandler)
    __dynamic_handlers__: List[Type[BaseErrorHandler]]

    __manager_handlers__: List[Type[BaseErrorHandler]] = []

    def __init__(self, higher_error_manager: 'BaseErrorManager' = None) -> None:
        self.higher_error_manager = higher_error_manager

        self._handlers = [
            handler_cls(self) for handler_cls in
            (self.__class__.__dynamic_handlers__ + self.__class__.__manager_handlers__)
        ]

    async def register_handler(self, handler_instance: BaseErrorHandler) -> None:
        if not isinstance(handler_instance, BaseErrorHandler):
            raise TypeError("handler_instance must be instance of BaseErrorHandler")

        self._handlers.append(handler_instance)

    def unregister_handler(self, handler_instance: BaseErrorHandler) -> None:
        self._handlers.remove(handler_instance)

    @staticmethod
    def manager_handler(*, exception_cls: Type[BaseException], **meta_kwargs):
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("You can use this decorator only with coroutine functions")

            @wraps(func)
            async def wrapper(h, *args, **kwargs):
                return await func(h.manager, *args, **kwargs, handler=h)

            return handler(exception_cls=exception_cls, **meta_kwargs)(wrapper)

        return decorator

    async def process_error(self, error: BaseException, update: Update) -> None:
        error_handler = find_in_list(self._handlers, lambda x: issubclass(type(error), x.exception_cls))

        if error_handler is not None:
            if await error_handler.handle(error, update):
                return
        if self.higher_error_manager:
            return await self.higher_error_manager.process_error(error, update)
        else:
            return await self.handle_unknown_error(error, update)

    @abstractmethod
    async def handle_unknown_error(self, error: BaseException, update: Update) -> None:
        ...


class ErrorManager(BaseErrorManager):
    async def handle_unknown_error(self, error: BaseException, update: Update) -> None:
        logger.error(f'Got unknown error while processing update[{update.id}]: {get_traceback_text(error)}')
        sys.stderr.write(get_traceback_text(error))
