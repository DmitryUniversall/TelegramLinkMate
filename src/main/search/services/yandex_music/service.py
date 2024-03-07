import re
from typing import Union, TYPE_CHECKING, Optional, Any
from ..service import Service
from src.main.search.exceptions import SearchFailedUserError
import logging

from src.main.search.data_types.data_source import DataSource

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from src.main.search.data_types.track import Track
    from src.main.search.data_types.playlist import Playlist


class YandexMusicService(Service):
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [YandexMusicService]>"

    async def get_from_url(self, url: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_url, get_tracks_from_album, get_tracks_from_playlist

        if re.search(r"album/\d+/track/\d+/?", url):
            return await get_track_from_url(
                url=url
            )
        elif match := re.search(r"users/(\S+?)/playlists/(\d+)", url):
            return await get_tracks_from_playlist(
                int(match.group(2)), match.group(1)
            )
        elif match := re.search(r"album/(\d+)/?", url):
            return await get_tracks_from_album(
                int(match.group(1))
            )
        else:
            logger.debug(f"Unknown url format: {url}")
            raise SearchFailedUserError(f'Неизвестный формат ссылки: {url}')

    async def get_from_name(self, name: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_name

        return await get_track_from_name(
            name=name
        )

    async def get_sources(self, url: str) -> DataSource:
        from .search import get_track_audio_sources, get_raw_track_from_url

        raw = await get_raw_track_from_url(url)
        return DataSource(
            audio_source=await get_track_audio_sources(track=raw),
            video_source=[]
        )

    async def get_lyrics(self, url: str) -> Optional[str]:
        from .search import get_track_lyrics, get_raw_track_from_url

        return await get_track_lyrics(
            track=await get_raw_track_from_url(url)
        )

    async def get_from_raw(self, raw: Any) -> 'Track':
        from .search import to_track

        return await to_track(
            raw_track=raw
        )

    async def get_sources_from_raw(self, raw: Any) -> DataSource:
        from .search import get_track_audio_sources

        return DataSource(
            audio_source=await get_track_audio_sources(raw),
            video_source=[]
        )


yandex_music_service = YandexMusicService()
