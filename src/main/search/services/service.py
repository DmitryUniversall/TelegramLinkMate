from abc import ABC, abstractmethod
from typing import Union, Optional, TYPE_CHECKING, Any

from ..data_types.data_source import DataSource

if TYPE_CHECKING:
    from ..data_types.track import Track
    from ..data_types.playlist import Playlist


class BaseService(ABC):
    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    async def get_from_url(self, url: str) -> Union['Track', 'Playlist']:
        ...

    @abstractmethod
    async def get_from_name(self, name: str) -> Union['Track', 'Playlist']:
        ...

    @abstractmethod
    async def get_sources(self, url: str) -> DataSource:
        ...

    @abstractmethod
    async def get_from_raw(self, raw: Any) -> 'Track':
        ...

    @abstractmethod
    async def get_sources_from_raw(self, raw: Any) -> DataSource:
        ...

    async def get_lyrics(self, url: str) -> Optional[str]:
        ...

    async def search(self, query: str) -> Optional[Union['Track', 'Playlist']]:
        if "https://" in query:
            return await self.get_from_url(query)
        else:
            return await self.get_from_name(query)


class Service(BaseService, ABC):
    pass
