import teleapi
from src.core.utils.text import strip_lines
from .commands import YandexCommand, YoutubeCommand, HelpCommand


class MainExecutor(teleapi.Executor):
    __executor_commands__ = [
        YandexCommand,
        YoutubeCommand,
        HelpCommand
    ]

    @teleapi.Executor.executor_command(name="start")
    async def start_command(self, message: teleapi.Message, **__) -> None:
        await message.reply(
            text=strip_lines(
                """
                <b>Добро пожаловать</b>
                
                Я - LinkMate бот. Готов помочь вам скачивать видео из youtube и музыку из yandex_music.
                
                🚀 <b>Как это работает</b> 🚀
                Пользоваться ботом совсем несложно:
                1. Просто укажите название или ссылку на музыку или видео, которые вы хотите загрузить.
                2. Выберите необходимое видео/трек 
                3. Скачивайте файл по прямой ссылке на хранилище google/yandex
                
                Используйте /help, чтобы узнать о функционале подробнее
                """
            ),
            parse_mode=teleapi.ParseMode.HTML
        )
