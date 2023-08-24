import asyncio
from typing import Union

import teleapi
from .search import search_manager, Track, Playlist
from .search.services import yandex_music_service, youtube_service
from .utils import strip_lines


class MainExecutor(teleapi.Executor):
    async def send_chat_action(self, chat: teleapi.Chat, action: teleapi.ChatAction, interval: int = 5):
        while True:
            await chat.send_action(action)
            await asyncio.sleep(interval)

    async def get_query_dialog(self, chat: teleapi.Chat) -> str:
        while True:
            await chat.send_message(
                text="Укажите примерное название или ссылку на Youtube видео/плейлист"
            )

            _, data = await self.wait_for(
                event_type=teleapi.UpdateEvent.ON_MESSAGE,
                filter_=lambda _, x: x['message'].chat == chat
            )

            msg = data['message']

            if msg.text:
                return msg.text

    async def send_search_result_message(self,
                                         message: teleapi.Message,
                                         obj: Union[Track, Playlist],
                                         message_to_edit: teleapi.Message = None,
                                         max_variations: int = 5
                                         ) -> None:
        async def format_track(track: Track) -> str:
            data_source = track.data_source if track.data_source.audio_source else await track.get_data_source()

            return strip_lines(
                f"""
                💿 <em><a href="{track.url}">{track.title}</a> - {'; '.join([f'<a href="{author.url}">{author.name}</a>' for author in track.authors])}</em>
                ├Вот <a href="{data_source.audio_source[0]}">ссылка</a> на скачивание аудио
                └{f'Вот <a href="{data_source.video_source[0]}">ссылка</a> на скачивание видео'
                if data_source.video_source else 'Ссылка на скачивание видео недоступна'}
                """,
                symbols=" "
            ).strip("\n")

        if isinstance(obj, Track):
            track_text = await format_track(obj)
            variations_text = "\n\n".join(
                list(await asyncio.gather(*[format_track(track) for track in obj.variations[:max_variations]])))

            if message_to_edit:
                await message_to_edit.edit_media(
                    media=teleapi.InputMediaPhoto(
                        media=obj.image_url,
                        caption=f"<b>Вот, что я нашел по вашему запросу:</b>\n\n{track_text}\n\n{variations_text}",
                        parse_mode=teleapi.ParseMode.HTML
                    )
                )
            else:
                await message.reply_photo(
                    photo=obj.image_url,
                    caption=f"<b>Вот, что я нашел по вашему запросу:</b>\n\n{track_text}\n\n{variations_text}",
                    parse_mode=teleapi.ParseMode.HTML,
                )

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

    @teleapi.Executor.executor_command(name='youtube')
    async def youtube_command(self, message: teleapi.Message, parameters, **_) -> None:
        query = " ".join(parameters)

        if len(query) == 0:
            query = await self.get_query_dialog(chat=message.chat)

        loading_image = await message.chat.send_photo(
            photo="https://dummyimage.com/600x400.jpg&text=Loading...#E4D9FF/fff",
            caption="<b>Пожалуйста, подождите:</b> Бот ищет информацию",
            parse_mode=teleapi.ParseMode.HTML
        )

        await message.chat.send_action(teleapi.ChatAction.TYPING)

        chat_action_task = asyncio.create_task(self.send_chat_action(message.chat, teleapi.ChatAction.TYPING))
        found = await search_manager.search(query=query, service=youtube_service)
        chat_action_task.cancel()

        await self.send_search_result_message(message, found.result, message_to_edit=loading_image)

    @teleapi.Executor.executor_command(name='yandex')
    async def test2_command(self, message: teleapi.Message, parameters, **_) -> None:
        query = " ".join(parameters)

        if len(query) == 0:
            query = await self.get_query_dialog(chat=message.chat)

        loading_image = await message.chat.send_photo(
            photo="https://dummyimage.com/600x400.jpg&text=Loading...#E4D9FF/fff",
            caption="<b>Пожалуйста, подождите:</b> Бот ищет информацию",
            parse_mode=teleapi.ParseMode.HTML
        )

        await message.chat.send_action(teleapi.ChatAction.TYPING)

        chat_action_task = asyncio.create_task(self.send_chat_action(message.chat, teleapi.ChatAction.TYPING))
        found = await search_manager.search(query=query, service=yandex_music_service)
        chat_action_task.cancel()

        await self.send_search_result_message(message, found.result, message_to_edit=loading_image)
