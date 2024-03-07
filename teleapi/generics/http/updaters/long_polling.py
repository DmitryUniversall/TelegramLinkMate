import asyncio
from typing import List

from teleapi.core.http.request import method_request
from teleapi.core.http.updaters import BaseUpdater
from teleapi.types.update.obj import Update
from teleapi.types.update.serializer import UpdateSerializer
from teleapi.core.http.request import APIMethod
from teleapi.core.utils.collections import clear_none_values
import logging

_logger = logging.getLogger(__name__)


class LongPollingUpdater(BaseUpdater):
    """
    The LongPollingUpdater class can be used for getting asynchronous updates via getUpdates method (long-polling).
    """

    def __init__(self, *, timeout: int = 60, offset: int = None, **kwargs) -> None:
        """
        Initialize a LongPollingUpdater instance.

        :param timeout: `int`
            Timeout in seconds for long-polling requests. Default is 60 seconds.

        :param offset: `int`
            (Optional) Offset identifier for fetching updates.
            If None, sets after first fetched update

        :param kwargs: `dict`
            (Optional) Other parameters to be passed to the parent class constructor.
        """

        super().__init__(**kwargs)
        self.timeout = timeout
        self.offset = offset

    async def get_updates(self) -> List[Update]:
        """
        Fetch updates from the API using long-polling and getUpdates method.

        :return: `List[Update]`
            Lust of fetched Update objects

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the fetched data contains incorrect data or serialization failed
        """

        params = clear_none_values({
            "timeout": self.timeout,
            "offset": self.offset,
            "allowed_updates": [upd.value for upd in self.allowed_updates] if self.allowed_updates else None
        })

        while True:
            attempt = 0

            try:
                response, data = await method_request('GET', APIMethod.GET_UPDATES, params=params)

                if len(data['result']) == 0:
                    return []

                updates = UpdateSerializer().serialize(data=data['result'], many=True)

                self.offset = updates[-1].id + 1
                return updates
            except Exception as error:
                _logger.debug(f"Unknown error while fetching updates (attempt {attempt}): {error.__class__.__name__}: {str(error)}")
                await asyncio.sleep(2)
                attempt += 1

                if attempt > 5:
                    _logger.critical(f"CRITICAL ERROR: {error.__class__.__name__}: {str(error)}")
                    raise error

                continue
