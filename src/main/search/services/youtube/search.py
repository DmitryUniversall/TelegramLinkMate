import json
import yt_dlp
from yt_dlp.utils import DownloadError
import asyncio
import logging
from teleapi import project_settings
from typing import Optional, Dict, Any, List, Iterable, Tuple
from teleapi.core.utils.errors import get_traceback_text

from src.main.search.data_types.data_source import DataSource
from src.main.search.exceptions import SearchFailedUserError
from src.main.search.data_types.track import Track
from src.main.search.data_types.playlist import Playlist
from src.main.search.data_types.author import Author
from concurrent.futures import ThreadPoolExecutor, Executor
from src.main.search.services.youtube.service import youtube_service
from teleapi.core.utils.async_tools import async_http_request
from src.main.search.utils.async_tools import run_in_executor

logger = logging.getLogger("src.music.search.YtdlpSearch")


def fetch_track_data(query: str) -> dict:
    with yt_dlp.YoutubeDL(project_settings.YTDLP_OPTIONS) as ytdl:
        try:
            return ytdl.extract_info(query if query.startswith("https://") else f"ytsearch3:{query}", download=False)
        except DownloadError:
            raise SearchFailedUserError(f"По запросу '{query}' ничего не найдено. Видео не найдено/скрыто/не доступно")


async def afetch_track_data(query: str, executor: Optional[Executor] = None) -> dict:
    return await run_in_executor(executor, fetch_track_data, query=query)


async def afetch_tracks_data(queries: List[str]) -> List[dict]:
    executor = ThreadPoolExecutor(max_workers=len(queries))

    return list(
        await asyncio.gather(*[
            afetch_track_data(query, executor=executor) for query in queries
        ])
    )


def playlist_from_ytdlp_object(data: dict, tracks: list[Track] = None) -> Playlist:
    playlist = Playlist(
        authors=[
            Author(
                service=youtube_service,
                name=data["channel"],
                url=data["channel_url"]
            )
        ],
        title=data["title"],
        service=youtube_service,
        url=data["webpage_url"]
    )

    if tracks:
        for track in tracks:
            playlist.add(track)

    return playlist


async def to_track(*, raw_track: Dict[str, Any], variations: List[Track] = None) -> Track:
    return Track(
        title=raw_track['title'],
        url=raw_track['webpage_url'],
        authors=[
            Author(
                service=youtube_service,
                url=raw_track['channel_url'],
                name=raw_track['channel'],
            )
        ],
        image_url=raw_track['thumbnail'],
        data_source=DataSource(
            audio_source=get_available_audio_sources_from_data(raw_track['formats']),
            video_source=get_available_video_sources_from_data(raw_track['formats'])
        ),
        service=youtube_service,
        variations=variations,
        raw=raw_track
    )


async def to_track_many(*, raw_tracks: Iterable[Dict[str, Any]]) -> List[Track]:
    return list(
        await asyncio.gather(*[
            to_track(
                raw_track=track_data
            ) for track_data in raw_tracks
        ])
    )


def get_available_audio_sources_from_data(formats: dict) -> list:
    return list(
        map(
            lambda x: x['url'],
            filter(
                lambda x: x['format_id'] == project_settings.AVAILABLE_YOUTUBE_SOUND_FORMAT, formats
            )
        )
    )


def get_available_video_sources_from_data(formats: dict) -> list:
    return list(
        map(
            lambda x: x['url'],
            filter(
                lambda x: x['format_id'] == project_settings.AVAILABLE_YOUTUBE_VIDEO_FORMAT, formats
            )
        )
    )


async def get_track_from_name(name: str) -> Track:
    if name.startswith("https://"):
        logger.warning(f"Got url ('{name}') in 'find_track_by_name' function")

    raw_track = await afetch_track_data(name)

    if len(raw_track['entries']) == 0:
        raise SearchFailedUserError(f"По запросу '{name}' ничего не найдено")

    return await to_track(
        raw_track=raw_track['entries'][0],
        variations=await to_track_many(
            raw_tracks=raw_track['entries'][1:]
        ) if len(raw_track['entries']) > 1 else None
    )


async def get_track_from_url(url: str) -> Track:
    if not url.startswith("https://"):
        logger.warning(f"Got unknown url ('{url}') in 'find_track_by_url' function")

    raw_track = await afetch_track_data(url)

    return await to_track(
        raw_track=raw_track
    )


async def get_playlist(url: str) -> Playlist:
    data = await afetch_track_data(url)

    tracks = await to_track_many(
        raw_tracks=data['entries']
    )

    return playlist_from_ytdlp_object(data, tracks)


async def get_track_lyrics_from_data(data: dict) -> Optional[str]:
    if not data:
        return

    try:
        subtitles_url = list(filter(lambda x: x['ext'].startswith("json"), list(data.values())[0]))[0]['url']
        response, subtitles_raw = await async_http_request("GET", subtitles_url)
        subtitles_json = json.loads(subtitles_raw)
        return "\n".join([event["segs"][0]["utf8"] for event in subtitles_json["events"]])
    except Exception as error:
        logger.warning(f"Got unknown error while trying to get track lyrics:\n{get_traceback_text(error)}")
        return


async def get_track_lyrics(url: str) -> Optional[str]:
    data = await afetch_track_data(url)

    return await get_track_lyrics_from_data(data['subtitles'])


async def get_track_sources(url: str) -> Tuple[List[str], List[str]]:
    data = await afetch_track_data(query=url)

    return get_available_audio_sources_from_data(data['formats']), get_available_video_sources_from_data(data['formats'])
