from typing import List

from src.main.search.data_types.track import Track
from src.main.search.data_types.playlist import Playlist
from src.main.search.services import YandexMusicService
from src.main.utils import strip_lines
from src.main.search import search_manager, SearchResult
import teleapi
import asyncio


def clear_text(string: str) -> str:
    return string.replace("<", "&lt").replace(">", "&gt")


async def format_track(track: Track, index: int = None) -> str:
    data_source = track.data_source

    return strip_lines(
        f"""
        💿 {f"{index} " if index is not None else ""}<em><a href="{track.url}">{clear_text(track.title)}</a> - {'; '.join([f'<a href="{author.url}">{clear_text(author.name)}</a>' for author in track.authors])}</em>
        ├Вот <a href="{data_source.audio_source[0]}">ссылка</a> на скачивание аудио
        └{f'Вот <a href="{data_source.video_source[0]}">ссылка</a> на скачивание видео'
        if data_source.video_source else 'Ссылка на скачивание видео недоступна'}
        """,
        symbols=" "
    ).strip("\n")


class SearchResultMessageView(teleapi.View):
    def __init__(self, search_result: SearchResult, max_tracks: int = 5) -> None:
        super().__init__()

        self.search_result = search_result
        self.max_tracks = max_tracks
        self.base_message_text = f"<b>Вот, что я нашел по вашему запросу:</b>\n\n"

    @teleapi.View.view_button(text='Я нашёл нужный трек/видео', row=0)
    async def right_track_button(self, callback_query: teleapi.CallbackQuery, **_) -> None:
        search_manager.cache_result(self.search_result)

        await self.message.edit_reply_markup(reply_markup=None)
        await callback_query.answer(text="Спасибо за отзыв!")


class PlaylistMessageView(SearchResultMessageView):
    def __init__(self, search_result: SearchResult, max_tracks: int = 5) -> None:
        super().__init__(search_result, max_tracks)

        self.playlist = search_result.result
        self.playlist_pages = [
            self.playlist.tracks[index: index + self.max_tracks] for index in
            range(0, len(self.playlist.tracks), self.max_tracks)
        ]

        self.page = 0

    @teleapi.View.view_button(text="⬅️ Назад", row=1, place=0)
    async def previous_button(self, callback_query: teleapi.CallbackQuery, **_) -> None:
        if self.page == 0:
            await callback_query.answer("Первая страница")
            return
        else:
            self.page -= 1

        await self.message.edit_caption(
            caption=await self.get_text(),
            parse_mode=teleapi.ParseMode.HTML,
            keep_reply_markup=True
        )

    @teleapi.View.view_button(text="Вперед ➡️", row=1, place=1)
    async def next_button(self, callback_query: teleapi.CallbackQuery, **_) -> None:
        if self.page == len(self.playlist_pages) - 1:
            await callback_query.answer("Последняя страница")
            return
        else:
            self.page += 1

        await self.message.edit_caption(
            caption=await self.get_text(),
            parse_mode=teleapi.ParseMode.HTML,
            keep_reply_markup=True
        )

    def get_page(self) -> List[Track]:
        return self.playlist_pages[self.page]

    async def get_text(self) -> str:
        tracks_text = "\n\n".join(
            list(
                await asyncio.gather(
                    *[
                        format_track(track) for track in self.get_page()
                    ]
                )
            )
        )

        return self.base_message_text + f"""<b>Плейлист {self.playlist.title}</b>\n\n{tracks_text}\n\n{f"Страница {self.page + 1}/{len(self.playlist_pages)}"}"""


class TrackMessageView(SearchResultMessageView):
    def __init__(self, search_result: SearchResult, max_tracks: int = 5) -> None:
        super().__init__(search_result, max_tracks)

        self.track = search_result.result

    async def get_text(self) -> str:
        track_text = await format_track(self.track)
        variations_text = "\n\n".join(
            list(
                await asyncio.gather(
                    *[
                        format_track(track) for track in self.track.variations[:self.max_tracks]
                    ]
                )
            )
        )

        return self.base_message_text + f"{track_text}\n\n{variations_text}"


async def send_search_result_message(search_result: SearchResult,
                                     chat: teleapi.Chat = None,
                                     message_to_edit: teleapi.Message = None,
                                     max_tracks: int = 3
                                     ) -> teleapi.Message:
    if not message_to_edit.photo:
        raise ValueError("message_to_edit must have photo to be edited")

    obj = search_result.result

    if obj is None:
        raise ValueError("Result is None")

    message_parse_mode = teleapi.ParseMode.HTML
    message_photo = obj.image_url

    if isinstance(obj, Track):
        view = TrackMessageView(search_result, max_tracks)
    elif isinstance(obj, Playlist):
        view = PlaylistMessageView(search_result, max_tracks)
    else:
        raise TypeError(f"Unknown result object type: {type(obj)}")

    message_text = await view.get_text()

    if isinstance(obj.service, YandexMusicService):
        message_text += "\n\n<b>Внимание:</b>\nУчитывайте, что ссылки на скачивание с YandexMusic истекают всего через 15 минут!"

    if message_to_edit:
        return await message_to_edit.edit_media(
            media=teleapi.InputMediaPhoto(
                media=message_photo,
                caption=message_text,
                parse_mode=message_parse_mode,
            ),
            view=view
        )
    else:
        return await chat.send_photo(
            photo=message_photo,
            caption=message_text,
            parse_mode=message_parse_mode,
            view=view
        )
