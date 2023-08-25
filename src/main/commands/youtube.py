import asyncio

import teleapi
from .utils import get_query_dialog, send_chat_action
from .messages import send_search_result_message
from src.main.search import search_manager
from src.main.search.services import youtube_service
from ..utils import strip_lines


class YoutubeCommand(teleapi.Command):
    class Meta:
        name = 'youtube'
        description = strip_lines(
            """
            <b>Поиск видео в YouTube</b>
            
            <b>Важно:</b>
            <i>- Бот поддерживает видео (по названию и ссылке) и плейлисты (по ссылке)</i>
            <i>- Ссылки на скачивание с Youtube истекают через 1 день</i>

            <b>Использование:</b>
            /youtube
            <i>А затем указать название/ссылку в следующем сообщении.</i>
            
            <b>ИЛИ</b>

            /youtube <i>Название видео/плейлиста или ссылка на него</i>
            <i>(Например: <code>/youtube Believer</code>)</i>
            """
        )
        photo = "https://www.onemorething.nl/wp-content/uploads/2016/06/youtube-logo-recht-16x9-1.png"

    async def execute(self, message: teleapi.Message, **kwargs) -> None:
        query = " ".join(kwargs.get('parameters'))

        if len(query) == 0:
            query = await get_query_dialog(self.executor, chat=message.chat)

        loading_image = await message.chat.send_photo(
            photo="https://dummyimage.com/600x400.jpg&text=Loading...#E4D9FF/fff",
            caption="<b>Пожалуйста, подождите:</b> Бот ищет информацию",
            parse_mode=teleapi.ParseMode.HTML
        )

        await message.chat.send_action(teleapi.ChatAction.TYPING)

        chat_action_task = asyncio.create_task(send_chat_action(message.chat, teleapi.ChatAction.TYPING))
        found = await search_manager.search(query=query, service=youtube_service)
        chat_action_task.cancel()

        await send_search_result_message(found, chat=message.chat, message_to_edit=loading_image)
