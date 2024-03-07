from abc import ABC, abstractmethod
from teleapi.types.update.obj import Update
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from teleapi.core.bots.bot import BaseBot


class BaseMiddleware(ABC):
    """
    Abstract BaseMiddleware class.
    Middleware can be used to pre-process and post-process updates before and after they are handled by the bot.
    """

    def __init__(self, bot: 'BaseBot') -> None:
        """
        Initialize the middleware.

        :param bot: `BaseBot`
            Bot, which middleware belongs to
        """

        self.bot = bot

    async def ainit(self) -> None:
        """
        Perform asynchronous initialization for the middleware.
        This method can be overridden by subclasses to perform any necessary setup.
        """
        ...

    @abstractmethod
    async def pre_process(self, update: Update) -> Update:
        """
        Pre-process the incoming update.

        :param update: `Update`
            The update received from the updater to be pre-processed.

        :return: `Update`
            The pre-processed update.
        """
        ...

    @abstractmethod
    async def post_process(self, update: Update) -> None:
        """
        Post-process the update after it has been handled by the bot.

        :param update: `Update`
            The update to be post-processed.
        """
        ...
