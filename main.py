import asyncio
import os

os.environ.setdefault("SETTINGS_MODULE", "config")

import logging
from teleapi.core.logs import setup_teleapi_logger, setup_logger
from src import MusicalBOBBot
import teleapi


async def main():
    setup_teleapi_logger(console_log_level=logging.DEBUG)
    setup_logger('src', console_log_level=logging.DEBUG)

    bot = MusicalBOBBot(teleapi.LongPollingUpdater)
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())
