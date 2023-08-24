import yandex_music
from typing import List, Tuple
import logging
from src.main.search.exceptions import NotFoundUserError, SearchFailedUserError


logger = logging.getLogger('bot.src.music.YandexMusicClient')
yandex_music.ClientAsync._ClientAsync__notice_displayed = True


class MyYMClient(yandex_music.ClientAsync):
    async def search_by_name(self: yandex_music.ClientAsync, query: str) -> List[yandex_music.Track]:
        result = await self.search(
            text=query,
            type_='track',
        )

        if not result.tracks:
            raise NotFoundUserError(f"По запросу '{query}' в Yandex Music ничего не найдено")

        return result.tracks.results

    async def get_tracks(self, tracks_data: dict, timeout: int = 5, attempts: int = 0) -> List[yandex_music.Track]:
        if attempts == 5:
            raise NotFoundUserError(f"Не удалось получить информацию о треке")

        try:
            return await self.tracks([f'{track_id}:{album_id}' for album_id, track_id in tracks_data.items()], timeout=timeout)
        except yandex_music.exceptions.TimeOutError:
            return await self.get_tracks(tracks_data, timeout, attempts + 1)

    async def get_album_tracks(self, album_id: int) -> Tuple[yandex_music.Album, List[yandex_music.Track]]:
        try:
            album = await self.albums_with_tracks(album_id)
            volume = album.volumes[0]
        except IndexError as error:
            logger.warning(
                f"Failed to get album tracks for album '{album_id}' [NOT FOUND]: {error}"
            )
            raise SearchFailedUserError(f"Альбом не найден")
        return album, volume
