import asyncio
import os

os.environ.setdefault("SETTINGS_MODULE", "config")

import logging
from teleapi.core.logs import setup_teleapi_logger, setup_logger
from src import MusicalBOBBot
import teleapi
from src.main.search.services.yandex_music.client import MyYMClient


async def main():
    client = MyYMClient(teleapi.project_settings.YANDEX_MUSIC_TOKEN)
    await client.init()

    teleapi.project_settings.YANDEX_MUSIC_CLIENT = client

    setup_teleapi_logger(console_log_level=logging.DEBUG)
    setup_logger('src', console_log_level=logging.DEBUG)

    bot = MusicalBOBBot(teleapi.LongPollingUpdater)
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())
