import re
from typing import Union, TYPE_CHECKING, Optional, Any
from ..service import Service
from ...data_types.data_source import DataSource
from src.main.search.exceptions import SearchFailedUserError
import logging

if TYPE_CHECKING:
    from ...data_types.track import Track
    from ...data_types.playlist import Playlist

logger = logging.getLogger(__name__)


class YoutubeService(Service):
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [YoutubeService]>"

    async def get_from_url(self, url: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_url, get_playlist

        if re.search(r"watch\?v=(\S{11})", url) or re.search(r"youtu\.be/(\S{11})", url):
            return await get_track_from_url(
                url=url
            )
        elif re.search(r"playlist\?list=(\S{34})", url):
            return await get_playlist(url)
        else:
            logger.debug(f"Неизвестный формат ссылки: {url}")
            raise SearchFailedUserError('Неизвестный формат ссылки')

    async def get_from_name(self, name: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_name

        return await get_track_from_name(
            name=name
        )

    async def get_sources(self, url: str) -> DataSource:
        from .search import get_track_sources

        audio_source, video_source = await get_track_sources(url)
        return DataSource(
            audio_source=audio_source,
            video_source=video_source
        )

    async def get_lyrics(self, url: str) -> Optional[str]:
        from .search import get_track_lyrics

        return await get_track_lyrics(
            url=url
        )

    async def get_from_raw(self, raw: Any) -> 'Track':
        from .search import to_track

        return await to_track(
            raw_track=raw
        )

    async def get_sources_from_raw(self, raw: Any) -> DataSource:
        from .search import get_available_video_sources_from_data, get_available_audio_sources_from_data

        return DataSource(
            audio_source=get_available_audio_sources_from_data(raw['formats']),
            video_source=get_available_video_sources_from_data(raw['formats'])
        )


youtube_service = YoutubeService()
