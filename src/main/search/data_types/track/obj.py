from .model import TrackModel
from ..musical_object import MusicalObject


class Track(TrackModel, MusicalObject):
    async def get_info(self) -> 'Track':
        return await self.service.get_from_url(self.url)
