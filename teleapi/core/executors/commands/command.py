import inspect
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from teleapi.core.utils.syntax import default
from teleapi.types.message import Message
from teleapi.core.utils.collections import clear_none_values

if TYPE_CHECKING:
    from teleapi.core.executors import BaseExecutor


class BaseCommand(ABC):
    class Meta:
        pass

    def __init__(self, executor: 'BaseExecutor', name: str = None) -> None:
        self.executor = executor
        self.name = default(name, getattr(self.__class__.Meta, "name", None))

        if self.name is None:
            raise AttributeError("You must define command name as static property in Meta or in __init__ parameters")

    @abstractmethod
    async def execute(self, message: Message, **kwargs) -> None:
        ...

    async def ainit(self) -> None:
        ...

    async def before(self, message: Message, **kwargs) -> None:
        ...

    async def after(self, message: Message, **kwargs) -> None:
        ...

    async def process_error(self, error: BaseException, message, **kwargs) -> None:
        raise error

    async def invoke(self, message: Message, **kwargs) -> None:
        await self.before(message, **kwargs)

        try:
            await self.execute(message, parameters=message.text.split(" ")[1:], **kwargs)
        except BaseException as error:
            await self.process_error(error, message, **kwargs)
        else:
            await self.after(message, **kwargs)


class Command(BaseCommand, ABC):
    pass


def command(*, name: str = None, attr_name: str = None, before=None, after=None, **meta_kwargs):
    def decorator(func):
        if not inspect.iscoroutinefunction(func):
            raise TypeError('You can use this decorator only with coroutine functions')

        meta = type("Meta", (object,), {'name': default(name, func.__name__), **meta_kwargs})

        command_cls = type(default(attr_name, func.__name__), (Command,), {
            "execute": func,
            "Meta": meta,
            **clear_none_values({
                "before": before,
                "after": after
            })
        })

        return command_cls

    return decorator
