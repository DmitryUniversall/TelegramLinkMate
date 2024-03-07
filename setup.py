import logging

# Load src modules
import src  # type: ignore
from src.core.loggers import LoggerBuilder
from teleapi.core.project_state import ProjectState
from teleapi.core.state import project_settings, ProjectSettings, PyModuleConfig, JsonFileConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.bot import LinkmateBot


def setup_settings() -> ProjectSettings:
    """
    Set up project settings by registering configurations.

    :return: `ProjectSettings`
        The initialized project settings.
    """

    project_settings.register_config(PyModuleConfig('src.config'))
    project_settings.register_config(JsonFileConfig(project_settings.SECRET_CONFIG_PATH))

    return project_settings


def setup_loggers() -> logging.Logger:
    """
    Set up logging configurations based on the project state.

    :return: `logging.Logger`
        The configured bot logger.
    """

    if project_settings.STATE == ProjectState.PRODUCTION:
        return (
            LoggerBuilder('src', logging.INFO)
            .enable_console(level=logging.DEBUG)
            .add_file(project_settings.BOT_DEBUG_LOG_FILE_PATH, level=logging.DEBUG)
            .add_file(project_settings.BOT_INFO_LOG_FILE_PATH, level=logging.INFO)
            .get()
        )

    return (
        LoggerBuilder('src', logging.DEBUG)
        .enable_console(level=logging.DEBUG)
        .get()
    )


async def setup_bot(**kwargs) -> 'LinkmateBot':
    """
    Initialize the bot asynchronously.

    :param kwargs: `Dict`
        Additional keyword arguments to be passed to bot class.
    """

    from src.bot import LinkmateBot

    bot = LinkmateBot(**kwargs)
    await bot.ainit()

    project_settings.BOT = bot
    return bot
