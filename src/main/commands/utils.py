import teleapi
import asyncio
from typing import Union
from src.main.search.data_types.track import Track
from src.main.search.data_types.playlist import Playlist
from src.main.search.services import YandexMusicService
from src.main.utils import strip_lines


async def send_chat_action(chat: teleapi.Chat, action: teleapi.ChatAction, interval: int = 5):
    while True:
        await chat.send_action(action)
        await asyncio.sleep(interval)


async def get_query_dialog(executor: teleapi.BaseExecutor, chat: teleapi.Chat) -> str:
    while True:
        await chat.send_message(
            text="Укажите примерное название или ссылку видео/трек/плейлист/альбом"
        )

        _, data = await executor.wait_for(
            event_type=teleapi.UpdateEvent.ON_MESSAGE,
            filter_=lambda _, x: x['message'].chat == chat
        )

        msg = data['message']

        if msg.text:
            return msg.text


async def send_search_result_message(message: teleapi.Message,
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

        message_text = f"<b>Вот, что я нашел по вашему запросу:</b>\n\n{track_text}\n\n{variations_text}"
        message_photo = obj.image_url
        message_parse_mode = teleapi.ParseMode.HTML

        if isinstance(obj.service, YandexMusicService):
            message_text += "\n\n<b>Внимание:</b>\nУчитывайте, что ссылки на скачивание с YandexMusic истекают всего через 15 минут!"

        if message_to_edit:
            await message_to_edit.edit_media(
                media=teleapi.InputMediaPhoto(
                    media=message_photo,
                    caption=message_text,
                    parse_mode=message_parse_mode
                )
            )
        else:
            await message.reply_photo(
                photo=message_photo,
                caption=message_text,
                parse_mode=message_parse_mode
            )
