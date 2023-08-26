import asyncio
import os

os.environ.setdefault("SETTINGS_MODULE", "config")

import logging
from teleapi.core.logs import setup_teleapi_logger, setup_logger
from src import MusicalBOBBot
import teleapi
from src.main.search.services.yandex_music.client import MyYMClient
from src.error_manager import BotErrorManager


async def main():
    client = MyYMClient(teleapi.project_settings.YANDEX_MUSIC_TOKEN)
    await client.init()

    teleapi.project_settings.YANDEX_MUSIC_CLIENT = client

    setup_teleapi_logger(
        logs_dir=teleapi.project_settings.PROCESS_LOG_DIR,
        create_files=not teleapi.project_settings.DEBUG,
        console_log_level=logging.DEBUG if teleapi.project_settings.DEBUG else logging.INFO
    )

    setup_logger(
        'src',
        logs_dir=teleapi.project_settings.PROCESS_LOG_DIR if not teleapi.project_settings.DEBUG else None,
        console_log_level=logging.DEBUG
    )

    bot = MusicalBOBBot(teleapi.LongPollingUpdater, error_manager=BotErrorManager())
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())
