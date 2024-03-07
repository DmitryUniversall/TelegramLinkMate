import asyncio
import inspect
import re
from asyncio import Event
from functools import wraps

from teleapi.core.http.updaters.events import UpdateEvent
from typing import TYPE_CHECKING, List, Type, Optional, Callable, Union, Tuple
from .commands import BaseCommand
from .commands import command as command_factory
from .events import BaseEventListener, EventListener
from teleapi.core.utils.collectors import CollectorMeta, collect_subclasses
from abc import ABCMeta
from teleapi.types.update import Update
from .events import event as event_factory
from teleapi.types.message import Message
from teleapi.core.utils.collections import find_in_list
from teleapi.core.exceptions.managers import BaseErrorManager, ErrorManager
import logging
from teleapi.types.callback_query import CallbackQuery
from teleapi.core.ui.inline_view.view import BaseInlineView
from ..utils.syntax import default

if TYPE_CHECKING:
    from teleapi.core.bots.bot import BaseBot

logger = logging.getLogger(__name__)


class ExecutorMeta(CollectorMeta, ABCMeta):
    _collector = {
        'func': collect_subclasses,
        'attributes': {
            BaseCommand: '__dynamic_commands__',
            BaseEventListener: '__dynamic_event_listeners__'
        }
    }


class BaseExecutor(metaclass=ExecutorMeta):
    # Dynamic generated properties, that collects event_listeners(BaseEventListener)
    __dynamic_event_listeners__: List[Type[BaseEventListener]]

    __executor_event_listeners__: List[Type[BaseEventListener]] = []

    def __init__(self, bot: 'BaseBot', error_manager: Type[BaseErrorManager] = None) -> None:
        self.bot = bot
        self.error_manager = default(error_manager, ErrorManager(higher_error_manager=self.bot.error_manager))

        self._event_listeners = [
            event_listener_cls(self) for event_listener_cls in (self.__class__.__dynamic_event_listeners__ + self.__class__.__executor_event_listeners__)
        ]

    @staticmethod
    def executor_event(*, attr_name: str = None, event_type: UpdateEvent, before=None, after=None, **meta_kwargs):
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('You can use this decorator only with coroutine functions')

            @wraps(func)
            async def wrapper(listener: EventListener, update: Update, **kwargs):
                return await func(listener.executor, **kwargs, update=update, lisnener=listener)

            return event_factory(event_type=event_type, attr_name=attr_name, before=before, after=after, **meta_kwargs)(wrapper)

        return decorator

    @staticmethod
    def executor_command(*, name: str = None, attr_name: str = None, before=None, after=None, **meta_kwargs):
        def decorator(func):
            if not inspect.iscoroutinefunction(func):
                raise TypeError('You can use this decorator only with coroutine functions')

            @wraps(func)
            async def wrapper(cmd: 'BaseCommand', message: Message, *args, **kwargs) -> None:
                return await func(cmd.executor, message, *args, **kwargs, command=cmd)

            return command_factory(name=name, attr_name=attr_name, before=before, after=after, **meta_kwargs)(wrapper)

        return decorator

    async def wait_for(self, event_type: UpdateEvent, callback: Optional[Callable] = None, filter_: Callable[[Update, dict], bool] = None) -> Union[Tuple[Update, dict], None]:
        e = Event()
        data = None

        async def wrapper(event_listener: BaseEventListener, update: Update, **kwargs) -> None:
            nonlocal data

            if filter_ is not None and not filter_(update, kwargs):
                return

            if callback:
                await callback(event_listener, update, **kwargs)
                event_listener.is_active = False
                return

            data = (update, kwargs)
            event_listener.is_active = False
            e.set()

        listener = event_factory(event_type=event_type, attr_name=f"WaitFor__{event_type}")(wraps(callback)(wrapper) if callback is not None else wrapper)
        await self.register_event_listener(listener(self))

        if callback is not None:
            return listener

        await e.wait()
        return data

    async def ainit(self) -> None:
        for event_listener in self._event_listeners:
            asyncio.create_task(event_listener.ainit())

    async def register_event_listener(self, event_listener: BaseEventListener) -> None:
        if not isinstance(event_listener, BaseEventListener):
            raise TypeError("event_listener must be instance of BaseEventListener")

        await event_listener.ainit()
        self._event_listeners.append(event_listener)
        logger.debug(f"Registered event_listener {event_listener} in {self}")

    def unregister_event_listener(self, event_listener: BaseEventListener) -> None:
        self._event_listeners.remove(event_listener)

    def set_error_manager(self, error_manager: BaseErrorManager):
        if not isinstance(error_manager, BaseErrorManager):
            raise TypeError("error_manager must be instance of BaseErrorManager")

        error_manager.higher_error_manager = self.bot.error_manager

        self.error_manager = error_manager
        logger.debug(f"Set new error_manager ({error_manager}) for {self}")

    def _clear_event_listeners(self) -> None:
        removed = []

        for event_listener in self._event_listeners[:]:
            if not event_listener.is_active:
                self.unregister_event_listener(event_listener)
                removed.append(event_listener)

        if len(removed) != 0:
            logger.debug(f"Cleared {len(removed)} inactive event_listeners in {self}")

    async def call_event(self, update: Update, event_type: UpdateEvent, **kwargs) -> None:
        self._clear_event_listeners()

        listeners_to_call = filter(lambda x: x.event_type == event_type, self._event_listeners)
        tasks = [event_listener.invoke(update, **kwargs) for event_listener in listeners_to_call]

        for task in asyncio.as_completed(tasks):
            try:
                await task
            except BaseException as error:
                await self.error_manager.process_error(error, update)

        self._clear_event_listeners()


class Executor(BaseExecutor):
    # Dynamic generated properties, that collects commands(BaseCommand)
    __dynamic_commands__: List[Type[BaseCommand]]

    __executor_commands__: List[Type[BaseCommand]] = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._commands = [
            command_cls(self) for command_cls in
            (self.__class__.__dynamic_commands__ + self.__class__.__executor_commands__)
        ]

    async def ainit(self) -> None:
        await super().ainit()

        for command in self._commands:
            asyncio.create_task(command.ainit())

    async def register_command(self, command: BaseCommand) -> None:
        if not isinstance(command, BaseCommand):
            raise TypeError("command must be instance of BaseExecutor")

        await command.ainit()
        self._commands.append(command)

    def unregister_command(self, command: BaseCommand) -> None:
        self._commands.remove(command)

    @BaseExecutor.executor_event(event_type=UpdateEvent.ON_COMMAND)
    async def core_command_event(self, message: Message, command_name: str, update: Update, **_) -> None:
        command: BaseCommand = find_in_list(self._commands, lambda x: x.name == command_name)

        if not command:
            return

        try:
            await command.invoke(message)
        except BaseException as error:
            await self.error_manager.process_error(error, update)

    @BaseExecutor.executor_event(event_type=UpdateEvent.ON_CALLBACK_QUERY)
    async def view_check_event(self, callback_query: CallbackQuery, update: Update, **_) -> None:
        if not callback_query.data:
            return

        match = re.search(r"^\[(\w{5})=(\w{5})]", callback_query.data)

        if not match:
            return

        view_id, button_id = match.groups()
        view = find_in_list(BaseInlineView.__created_views__, lambda x: x.id == view_id)

        if view is None:
            logger.debug(f"Skipping view_check_callback_query_event (UpdateEvent.ON_CALLBACK_QUERY) because view with id '{view_id}' was not found")
            return

        try:
            await view.on_click(button_id, callback_query)
        except BaseException as error:
            await self.error_manager.process_error(error, update)
