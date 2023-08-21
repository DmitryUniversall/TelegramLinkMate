import re
from typing import Union, List, TYPE_CHECKING, Optional
from ..service import Service
from src.main.search.exceptions import SearchFailedUserError
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ...data_types.track import Track
    from ...data_types.playlist import Playlist


class YandexMusicService(Service):
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [YandexMusicService]>"

    async def get_from_url(self, url: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_url, get_tracks_from_album, get_tracks_from_playlist

        if re.search(r"album/\d+/track/\d+/?$", url):
            return await get_track_from_url(
                url=url
            )
        elif match := re.search(r"users/(\S+?)/playlists/(\d+)", url):
            return await get_tracks_from_playlist(
                int(match.group(2)), match.group(1)
            )
        elif match := re.search(r"album/(\d+)/?$", url):
            return await get_tracks_from_album(
                int(match.group(1))
            )
        else:
            logger.debug(f"Unknown url format: {url}")
            raise SearchFailedUserError(f'Неизвестный формат ссылки: {url}')

    async def get_from_name(self, query: str) -> Union['Track', 'Playlist']:
        from .search import get_track_from_name

        return await get_track_from_name(
            query=query
        )

    async def get_audio_sources(self, url: str) -> List[str]:
        from .search import get_track_audio_sources

        return await get_track_audio_sources(
            track=await self.get_from_url(url)
        )

    def get_lyrics(self, url: str) -> Optional[str]:
        from .search import get_track_lyrics

        return await get_track_lyrics(
            track=await self.get_from_url(url)
        )


yandex_music_service = YandexMusicService()
