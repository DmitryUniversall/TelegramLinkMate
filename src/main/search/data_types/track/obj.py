from .model import TrackModel
from ..data_source import DataSource
from ..musical_object import MusicalObject


class Track(TrackModel, MusicalObject):
    async def get_info(self) -> 'Track':
        return await self.service.get_from_url(self.url)

    async def get_data_source(self) -> DataSource:
        return await self.service.get_sources(url=self.url)
