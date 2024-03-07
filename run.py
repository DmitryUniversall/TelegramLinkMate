import teleapi
import asyncio
from src.error_manager import BotErrorManager
from setup import setup_bot, setup_loggers, setup_settings


async def main():
    settings = setup_settings()
    logger = setup_loggers()
    logger.info(f"Successful logger and settings setup")

    logger.info(f"Creating bot instance")
    bot = await setup_bot(
        updater_cls=teleapi.LongPollingUpdater,
        error_manager=BotErrorManager()
    )
    logger.info(f"Connected to Telegram as '{bot.me.username}'")

    logger.info(f"Starting bot with state: {settings.STATE}")
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())
