import asyncio

import teleapi

from src.main.search import search_manager
from src.main.search.services import yandex_music_service
from .utils import get_query_dialog, send_chat_action
from .messages import send_search_result_message
from ..utils import strip_lines


class YandexCommand(teleapi.Command):
    class Meta:
        name = 'yandex'
        description = strip_lines(
            """
            <b>Поиск треков в Yandex Music</b>
            
            <b>Важно:</b>
            <i>- Бот поддерживает треки (по названию и ссылке), плейлисты (по ссылке) и альбомы (по ссылке).</i>
            <i>- Ссылки на скачивание с Yandex Music истекают через 15 минут</i>
            
            <b>Использование:</b>
            /yandex
            <i>А затем указать название/ссылку в следующем сообщении.</i>
            
            <b>ИЛИ</b>
            
            /yandex <i>Название трека/плейлиста или ссылка на него</i>
            <i>(Например: <code>/yandex Believer</code>)</i>
            """
        )
        photo = "https://tustreams.com/tu-streams/assets/img/logos/yandex-music.jpg"

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
        found = await search_manager.search(query=query, service=yandex_music_service)
        chat_action_task.cancel()

        await send_search_result_message(found, chat=message.chat, message_to_edit=loading_image)
