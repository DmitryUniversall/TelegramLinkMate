import asyncio
import os

os.environ.setdefault("SETTINGS_MODULE", "config")

import logging
from teleapi.core.logs import setup_teleapi_logger
from src.bot import MusicalBOBBot
import teleapi


async def main():
    bot = MusicalBOBBot(teleapi.LongPollingUpdater)
    await bot.run()


if __name__ == '__main__':
    setup_teleapi_logger(console_log_level=logging.DEBUG)

    asyncio.run(main())
