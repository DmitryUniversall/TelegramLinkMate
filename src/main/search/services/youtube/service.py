from typing import Union, List, TYPE_CHECKING
from ..service import Service

if TYPE_CHECKING:
    from ...data_types.track import Track
    from ...data_types.playlist import Playlist


class YoutubeService(Service):
    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [YoutubeService]>"

    def get_from_url(self, url: str) -> Union['Track', 'Playlist']:
        pass

    def get_from_name(self, name: str) -> Union['Track', 'Playlist']:
        pass

    def get_audio_sources(self, url: str) -> List[str]:
        pass


youtube_service = YoutubeService()
