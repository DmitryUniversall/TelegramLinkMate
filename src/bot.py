import teleapi
from .main import MainExecutor
from src.main.search.services.yandex_music.client import MyYMClient


class LinkmateBot(teleapi.Bot):
    __bot_executors__ = [
        MainExecutor
    ]

    async def ainit(self) -> None:
        await super().ainit()

        client = MyYMClient(teleapi.project_settings.YANDEX_MUSIC_TOKEN)
        await client.init()

        teleapi.project_settings.YANDEX_MUSIC_CLIENT = client
