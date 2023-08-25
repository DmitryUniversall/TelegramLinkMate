import asyncio
import logging
import re
from typing import List, Optional, Union

import yandex_music

from src.main.search.exceptions import SearchFailedUserError
from src.main.search.data_types.track import Track
from src.main.search.data_types.author import Author
from src.main.search.data_types.playlist import Playlist
from src.main.search.data_types.data_source import DataSource
from .service import yandex_music_service
from teleapi import project_settings

logger = logging.getLogger('src.music.search.YandexSearch')


def author_from_yandex_object(obj: Union[yandex_music.Artist, yandex_music.User]):
    if isinstance(obj, yandex_music.Artist):
        return Author(
            name=obj.name,
            url=f"https://music.yandex.ru/artist/{obj.id}",
            service=yandex_music_service
        )
    elif isinstance(obj, yandex_music.User):
        return Author(
            name=obj.name,
            url=f"https://music.yandex.ru/users/{obj.login}/",
            service=yandex_music_service
        )
    else:
        logger.warning(f"Unknown author yandex object '{type(obj)}'")

        return Author(
            name="Unknown Artist",
            url=f"https://music.yandex.ru/",
            service=yandex_music_service
        )


def playlist_from_yandex_object(obj: Union[yandex_music.Album, yandex_music.Playlist],
                                tracks: List[Track] = None) -> Playlist:
    if isinstance(obj, yandex_music.Album):
        yandex_album: yandex_music.Album = obj

        playlist = Playlist(
            service=yandex_music_service,
            authors=[author_from_yandex_object(author) for author in yandex_album.artists],
            title=yandex_album.title,
            image_url=f'https://{yandex_album.cover_uri.replace("%%", "400x300")}',
            url=f"https://music.yandex.ru/album/{yandex_album.id}"
        )
    elif isinstance(obj, yandex_music.Playlist):
        yandex_playlist: yandex_music.Playlist = obj

        playlist = Playlist(
            service=yandex_music_service,
            authors=[author_from_yandex_object(yandex_playlist.owner)],
            title=yandex_playlist.title,
            image_url=f'https://{yandex_playlist.cover.uri.replace("%%", "400x400")}' if yandex_playlist.cover.uri else None,
            url=f"https://music.yandex.ru/users/{yandex_playlist.owner.login}/playlists/{yandex_playlist.kind}"
        )
    else:
        raise TypeError(f"Unknown yandex_playlist type: '{type(obj)}'")

    if tracks:
        for track in tracks:
            playlist.add(track)

    return playlist


async def to_track(*, raw_track: yandex_music.Track, variations: List[Track] = None) -> Track:
    return Track(
        title=raw_track.title,
        url=get_track_url(raw_track),
        duration=f'{raw_track.duration_ms // 60}:{raw_track.duration_ms % 60}',
        authors=[
            author_from_yandex_object(artist) for artist in raw_track.artists
        ],
        image_url=f'https://{raw_track.cover_uri.replace("%%", "400x300")}',
        data_source=DataSource(
            audio_source=await get_track_audio_sources(raw_track),
            video_source=[]
        ),
        service=yandex_music_service,
        variations=variations,
        raw=raw_track
    )


async def get_tracks_from_album(album_id: int) -> Playlist:
    album, raw_tracks = await project_settings.YANDEX_MUSIC_CLIENT.get_album_tracks(album_id)

    if not all((album, raw_tracks)):
        raise SearchFailedUserError('Не удалось получить список треков альбома')

    tracks = list(await asyncio.gather(*[to_track(raw_track=track) for track in raw_tracks]))

    return playlist_from_yandex_object(
        obj=album,
        tracks=tracks
    )


async def get_tracks_from_playlist(kind: int, username: str) -> Playlist:
    try:
        playlist = await project_settings.YANDEX_MUSIC_CLIENT.users_playlists(kind=kind, user_id=username)
    except yandex_music.exceptions.NotFoundError:
        raise SearchFailedUserError('Плейлист не найден или является приватным')

    full_raw_tracks = await asyncio.gather(*[
        short_track.fetch_track_async() for short_track in playlist.tracks
    ])

    tracks = list(await asyncio.gather(*[to_track(raw_track=raw_track) for raw_track in full_raw_tracks]))

    return playlist_from_yandex_object(
        obj=playlist,
        tracks=tracks
    )


async def get_track_from_name(name: str) -> Track:  # TODO: timeout
    tracks = await project_settings.YANDEX_MUSIC_CLIENT.search_by_name(name)

    return await to_track(
        raw_track=tracks[0],
        variations=list(
            await asyncio.gather(*[
                to_track(raw_track=raw_track) for raw_track in tracks[1:]
            ]) if len(tracks) > 1 else None
        )
    )


async def get_track_from_url(url: str) -> Track:
    raw_track = await get_raw_track_from_url(url)
    return await to_track(raw_track=raw_track, variations=None)


async def get_raw_track_from_url(url: str) -> yandex_music.Track:
    data = {}

    if match := re.search(r"album/(\d+)/track/(\d+)/?$", url):
        data[match.group(1)] = match.group(2)
    else:
        raise SearchFailedUserError(f"Неверный формат ссылки: {url}")

    raw_track = (await project_settings.YANDEX_MUSIC_CLIENT.get_tracks(data, timeout=10))[0]
    return raw_track


async def get_track_audio_sources(track: yandex_music.Track) -> List[str]:
    try:
        download_info = await track.get_download_info_async()
        download_info = download_info[0]

        return [await download_info.get_direct_link_async()]
    except IndexError as error:
        logger.debug(
            f"Failed to find audio source for track '{track.title} - {track.id}' [NOT FOUND]: {error}"
        )
        return []


async def get_track_lyrics(track: yandex_music.Track) -> Optional[str]:
    supplement = await track.get_supplement()

    if lyrics := supplement.lyrics:
        return lyrics.full_lyrics


def get_track_url(track: yandex_music.Track) -> str:
    return f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}"
