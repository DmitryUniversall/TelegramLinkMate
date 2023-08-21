import teleapi
from .main import MainExecutor


class MusicalBOBBot(teleapi.Bot):
    __bot_executors__ = [
        MainExecutor
    ]
