from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from teleapi.core.http.updaters.events import AllowedUpdates, AllowedUpdates_default
from teleapi.core.utils.syntax import default

if TYPE_CHECKING:
    from teleapi.core.bots.bot import BaseBot
    from teleapi.types.update.obj import Update


class BaseUpdater(ABC):
    """
    Base abstract class for updaters. Updaters are used for getting updates from telegram http api via one of the possible ways
    """

    def __init__(self, *, bot: 'BaseBot', allowed_updates: List[AllowedUpdates] = None) -> None:
        """
        Initialize a BaseUpdater instance.

        :param bot: `BaseBot`
            Bot, which updater belongs to

        :param allowed_updates: `List[AllowedUpdates]`
            (Optional) List of the update types you want your bot to receive.
            Defaults to AllowedUpdates_default

            This parameter doesn't affect updates created before the call to the getUpdates,
            so unwanted updates may be received for a short period of time.
        """

        self.bot = bot
        self.allowed_updates = default(allowed_updates, AllowedUpdates_default)

    async def ainit(self) -> None:
        """
        Method used for async initialize updater
        """
        ...

    @abstractmethod
    async def get_updates(self) -> List['Update']:
        """
        Fetches updates from the API using one of the possible ways

        :return: `List[Update]`
            Lust of fetched Update objects
        """
        ...


class Updater(BaseUpdater, ABC):
    pass
