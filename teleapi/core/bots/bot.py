import asyncio
from teleapi.core.http.updaters.updater import BaseUpdater
from teleapi.core.http.updaters.events import UpdateEvent, AllowedUpdates
from typing import Type, List, Dict
from teleapi.core.bots.middlewares import BaseMiddleware
from teleapi.core.utils.syntax import default
from teleapi.generics.http.methods.bot import get_me
from teleapi.types.chat.chat_type import ChatType
from teleapi.types.update.obj import Update
from abc import ABC, abstractmethod
from teleapi.core.executors.executor import BaseExecutor
from teleapi.core.state.settings import project_settings
import re
from teleapi.core.exceptions.managers import BaseErrorManager, ErrorManager
import logging
from teleapi.types.bot import TelegramBotObject
# from teleapi.core.logs import log_async_methods

logger = logging.getLogger(__name__)


# @log_async_methods()
class BaseBot(TelegramBotObject, ABC):
    """
    Abstract base class for creating bot instances. Starts and controls all bot activity
    """

    __bot_middlewares__: List[Type[BaseMiddleware]] = []
    __bot_executors__: List[Type[BaseExecutor]] = []

    def __init__(self, updater_cls: Type[BaseUpdater], error_manager: BaseErrorManager = None, allowed_updates: List[AllowedUpdates] = None) -> None:
        """
        Initialize the BaseBot instance.

        :param updater_cls: `Type[BaseUpdater]`
            The updater class responsible for fetching updates.

        :param error_manager: `type`
            The error manager for handling bot errors.
            If None, creates new ErrorManager

        :param allowed_updates: `type`
             List of the update types you want your bot to receive. Will be passed to updater_cls
        """

        self._is_initialized = False
        self.me = None
        self.error_manager = default(error_manager, ErrorManager())
        project_settings.BOT = self

        self._updater = updater_cls(bot=self, allowed_updates=allowed_updates)

        self.__middlewares: List[BaseMiddleware] = [
            middleware_cls(self) for middleware_cls in (project_settings.get('MIDDLEWARES', []) + self.__class__.__bot_middlewares__)
        ]
        self._executors: List[BaseExecutor] = [
            executor_cls(self) for executor_cls in (project_settings.get('EXECUTORS', []) + self.__class__.__bot_executors__)
        ]

    @abstractmethod
    async def dispatch(self, update: Update) -> None:
        """
        Abstract method to handle update and call events (UpdateEvent) that will be handled by all bot executors

        :param update: `Update`:
            The update received from the updater.
        """
        ...

    def get_regex_command_prefix(self) -> Dict[str, str]:
        """
        Abstract method to handle update and call an event (UpdateEvent) that will be handled by all bot executors

        :return: `Dict[str, str]`
            Dict with regex patterns that bot will use for recognize command in a message.
            Must contain 'group' and 'private' fields
        """

        return {
            'group': f"^/(\w+)@{self.me.username}",
            'private': f'^/(\w+)'
        }

    async def ainit(self) -> None:
        """
        Async initialize bot.

        Notes:
         - You must call super() if you need to override this method.
         - Method can be called only one time
        """

        if self._is_initialized:
            raise RuntimeError('Bot is already initialized')

        await self._updater.ainit()

        self.me = await get_me()

        for middleware in self.__middlewares:
            await middleware.ainit()

        for executor in self._executors:
            asyncio.create_task(executor.ainit())

        logger.info(f"Bot was successfully initialized")
        self._is_initialized = True

    async def register_executor(self, executor: BaseExecutor) -> None:
        """
        Registers new executor

        :param executor: `BaseExecutor`
            Executor to be registered

        :raises:
            :raise TypeError: if executor is not instance of BaseExecutor

        Notes:
         - Method calls executor.ainit when registering, so you should not call it manually
        """

        if not isinstance(executor, BaseExecutor):
            raise TypeError("executor must be instance of BaseExecutor")

        await executor.ainit()
        self._executors.append(executor)

        logger.debug(f"Registered executor {executor} ({type(executor)})")

    def unregister_executor(self, executor: BaseExecutor) -> None:
        """
        Unregisters executor

        :param executor: `BaseExecutor`
            Executor to be unregistered

        :raises:
            :raise ValueError: if executor is not in bot executors list
        """

        self._executors.remove(executor)

        logger.debug(f"Unregistered executor {executor}")

    async def register_middleware(self, middleware: BaseMiddleware) -> None:
        """
        Registers new middleware

        :param middleware: `BaseMiddleware`
            Middleware to be registered

        :raises:
            :raise TypeError: if middleware is not instance of BaseMiddleware

        Notes:
         - Method calls middleware.ainit when registering, so you should not call it manually
        """

        if not isinstance(middleware, BaseMiddleware):
            raise TypeError("middleware must be instance of BaseMiddleware")

        await middleware.ainit()
        self.__middlewares.append(middleware)

        logger.debug(f"Registered middleware {middleware} ({type(middleware)})")

    def unregister_middleware(self, middleware: BaseMiddleware) -> None:
        """
        Unregisters middleware

        :param middleware: `BaseMiddleware`
            Middleware to be unregistered

        :raises:
            :raise ValueError: if middleware is not in bot middlewares list
        """

        self.__middlewares.remove(middleware)

        logger.debug(f"Unregistered middleware {middleware}")

    async def call_event(self, update: Update, event_type: UpdateEvent, **kwargs) -> None:
        """
        Calls an event (UpdateEvent) in all bot executors

        :param update: `Update`
            The update received from the updater to be passed to executors

        :param event_type: `UpdateEvent`
            Event type to be passed to executors

        Notes:
         - All errors that was not processed in executor error_manager will be processed in bot error_manager
        """

        logger.debug(f"Calling event {event_type} on update {update.id}")

        tasks = [executor.call_event(update, event_type, **kwargs) for executor in self._executors]

        for task in asyncio.as_completed(tasks):
            try:
                await task
            except BaseException as error:
                asyncio.create_task(self.error_manager.process_error(error, update))

    async def process_update(self, update: Update) -> None:
        """
        Processed the update. Calls middleware and `self.dispatch` function

        :param update: `Update`
            The update received from the updater
        """

        logger.info(f"Processing update {update.id}")

        for middleware in self.__middlewares:
            update = await middleware.pre_process(update)

        await self.dispatch(update)

        for middleware in self.__middlewares:
            await middleware.post_process(update)

    async def _invoke_update(self, update: Update) -> None:
        """
        Calls `self.process_update` function and catches errors. Errors will be processed in bot error_manager

        :param update: `Update`
            The update received from the updater
        """

        if not self._is_initialized:
            raise RuntimeError("Bot is not initialized yet. Call 'ainit' method before use this")

        try:
            await self.process_update(update)
        except BaseException as error:
            await self.error_manager.process_error(error, update)

    async def run(self) -> None:
        """
        Starts the bot. Calls `self.ainit` if needed to.
        Get updates from `self.updater` and process them in `self._invoke_update`
        """

        logger.info(f"Starting bot with debug: {project_settings.DEBUG}")

        if not self._is_initialized:
            await self.ainit()

        while True:
            updates = await self._updater.get_updates()

            if updates:
                for update in updates:
                    asyncio.create_task(self._invoke_update(update))


class Bot(BaseBot):
    """
    An object from which the user should inherit for customization.
    Implements `dispatch` method
    """

    async def dispatch(self, update: Update) -> None:
        """
        Handles update and call events (UpdateEvent) that will be handled by all bot executors

        :param update: `Update`:
            The update received from the updater.
        """

        if update.message:
            if update.message.text and update.message.entities and update.message.entities[0].type_ == 'bot_command' and update.message.entities[0].offset == 0:
                if update.message.chat.type_ == ChatType.PRIVATE:
                    if match := re.match(self.get_regex_command_prefix()['private'], update.message.text):
                        asyncio.create_task(
                            self.call_event(update, UpdateEvent.ON_COMMAND, message=update.message, command_name=match.group(1))
                        )
                else:
                    if match := re.match(self.get_regex_command_prefix()['group'], update.message.text):
                        asyncio.create_task(
                            self.call_event(update, UpdateEvent.ON_COMMAND, message=update.message, command_name=match.group(1))
                        )

            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_MESSAGE, message=update.message)
            )
        if update.channel_post:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHANNEL_POST, post=update.channel_post)
            )
        if update.callback_query:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CALLBACK_QUERY, callback_query=update.callback_query)
            )
        if update.chat_member:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHAT_MEMBER_UPDATED, member_update=update.chat_member)
            )
        if update.bot_chat_member:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_BOT_CHAT_MEMBER_UPDATED, bot_member_update=update.bot_chat_member)
            )
        if update.poll:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_POLL_STATUS_UPDATED, poll=update.poll)
            )
        if update.poll_answer:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_POLL_ANSWER, answer=update.poll_answer)
            )
        if update.chat_join_request:
            asyncio.create_task(
                self.call_event(update, UpdateEvent.ON_CHAT_JOIN_REQUEST, answer=update.chat_join_request)
            )
