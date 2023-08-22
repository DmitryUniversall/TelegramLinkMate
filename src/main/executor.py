import asyncio
from typing import Union

import teleapi
from .search import search_manager, Track, Playlist
from .search.services import yandex_music_service, youtube_service
from .utils import strip_lines


class MainExecutor(teleapi.Executor):
    async def send_search_result_message(self,
                                         message: teleapi.Message,
                                         obj: Union[Track, Playlist],
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
            variations_text = "\n\n".join(list(await asyncio.gather(*[format_track(track) for track in obj.variations[:max_variations]])))

            await message.reply_photo(
                photo=obj.image_url,
                caption=f"<b>Вот, что я нашел по вашему запросу:</b>\n\n{track_text}\n\n{variations_text}",
                parse_mode=teleapi.ParseMode.HTML,
            )

    @teleapi.Executor.executor_command(name='youtube_search')
    async def test_command(self, message: teleapi.Message, parameters, **_) -> None:
        query = " ".join(parameters)

        if len(query) == 0:
            while True:
                # TODO: Кнопа отмены (диалога)
                # TODO: (teleapi) Придумать систему диалога
                await message.reply(
                    text="Укажите примерное название или ссылку на Youtube видео/плейлист"
                )

                _, data = await self.wait_for(
                    event_type=teleapi.UpdateEvent.ON_MESSAGE,
                    filter_=lambda _, x: x['message'].chat == message.chat
                )

                msg = data['message']

                if message.text:
                    query = msg.text
                    break

        # TODO: Не отправлять новое сообщение, а изменять это
        # TODO: (teleapi) edit_media and other edit*
        # TODO: (teleapi) delete message
        await message.chat.send_message(
            text="<b>Пожалуйста, подождите:</b> Бот ищет информацию",
            parse_mode=teleapi.ParseMode.HTML
        )
        await message.chat.send_action(teleapi.ChatAction.TYPING)  # TODO: Кидать каждые 5 сек если бот всё ещё ищет

        found = await search_manager.search(query=query, service=youtube_service)

        await self.send_search_result_message(message, found.result)

    @teleapi.Executor.executor_command(name='yandex_search')
    async def test2_command(self, message: teleapi.Message, parameters, **_) -> None:
        found = await search_manager.search(query=" ".join(parameters), service=yandex_music_service)

        await self.send_search_result_message(message, found.result)
