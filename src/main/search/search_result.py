from typing import List, Union, TYPE_CHECKING, Optional
from uuid import uuid4

if TYPE_CHECKING:
    from .data_types.playlist import Playlist
    from .data_types.track import Track


class SearchResult:
    def __init__(self, query: str, service: str) -> None:
        self.query = query
        self.service = service
        self.uuid = uuid4()
        self._result = None

    @property
    def result(self) -> Optional[List[Union[Track, Playlist]]]:
        return self._result

    @result.setter
    def result(self, value: List[Union[Track, Playlist]]) -> None:
        self._result = value

    def is_simular(self, query: str, service: str) -> bool:
        return query == self.query and service == self.service

    def __eq__(self, other) -> bool:
        return isinstance(other, SearchResult) and other.uuid == self.uuid
