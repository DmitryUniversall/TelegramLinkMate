import inspect
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from teleapi.core.exceptions.teleapi import CancelOperationError
from teleapi.core.http.updaters.events import UpdateEvent
from teleapi.core.utils.syntax import default
from teleapi.types.update import Update
from teleapi.core.utils.collections import clear_none_values

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from teleapi.core.executors import BaseExecutor


class BaseEventListener(ABC):
    class Meta:
        pass

    def __init__(self, executor: 'BaseExecutor', event_type: UpdateEvent = None) -> None:
        self.executor = executor
        self.is_active = True
        self.event_type = default(event_type, getattr(self.__class__.Meta, "event_type", None))

        if self.event_type is None:
            raise AttributeError(
                "You must define event listener event_type as static property in Meta or in __init__ parameters")

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{self.event_type};{self.executor}]>"

    @abstractmethod
    async def event_callback(self, update: Update, **kwargs) -> None:
        ...

    async def before(self, update: Update, **kwargs) -> None:
        ...

    async def after(self, update: Update, **kwargs) -> None:
        ...

    async def invoke(self, update: Update, **kwargs) -> None:
        try:
            await self.before(update, **kwargs)
        except CancelOperationError:
            logger.debug(f'Cancelling event call in {self}')
            return

        await self.event_callback(update, **kwargs)

        await self.after(update, **kwargs)

    async def ainit(self) -> None:
        ...


class EventListener(BaseEventListener, ABC):
    pass


def event(*, attr_name: str = None, event_type: UpdateEvent, before=None, after=None, **meta_kwargs):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError('You can use this decorator only with coroutine functions')

        meta = type("Meta", (object,), {'event_type': event_type, **meta_kwargs})

        event_listener_cls = type(default(attr_name, func.__name__), (EventListener,), {
            "event_callback": func,
            "Meta": meta,
            **clear_none_values({
                'before': before,
                'after': after
            })
        })

        return event_listener_cls

    return decorator
