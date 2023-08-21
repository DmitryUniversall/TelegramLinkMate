from .model import PlaylistModel
from ..musical_object import MusicalObject
from ..track import Track


class Playlist(PlaylistModel, MusicalObject):
    async def get_info(self) -> 'Playlist':
        return await self.service.get_from_url(self.url)

    def add(self, track: Track) -> None:
        if not isinstance(track, Track):
            raise TypeError("track must be of type Track")

        self.tracks.append(track)
