import asyncio

import teleapi
from .utils import get_query_dialog, send_chat_action, send_search_result_message
from src.main.search import search_manager
from src.main.search.services import yandex_music_service


class YandexCommand(teleapi.Command):
    class Meta:
        name = 'yandex'

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

        await send_search_result_message(message, found.result, message_to_edit=loading_image)
