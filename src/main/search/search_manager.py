from typing import List, Optional
from .search_result import SearchResult
from .services.service import BaseService
from .services import yandex_music_service, youtube_service
import logging

logger = logging.getLogger(__name__)


class BaseSearchManager:
    def __init__(self, max_cache_size: int = 100) -> None:
        self.__cache: List[SearchResult] = []
        self.max_cache_size = max_cache_size

    def cache_result(self, search_result: SearchResult) -> None:
        if not search_result.result:
            raise ValueError("SearchResult has not 'result'")

        self.__cache.append(search_result)

    def find_cached(self, query: str, service: str) -> Optional[SearchResult]:
        for result in self.__cache:
            if result.is_simular(query, service):
                logger.debug(f"Found cached search result for ['{query}': {service}]")
                return result

    async def search(self, query: str, service: BaseService = None, use_cache: bool = True) -> SearchResult:
        if use_cache and (result := self.find_cached(query, str(service))):
            return result

        if service is None:
            if "music.yandex.ru" in query:
                service = yandex_music_service
            else:
                service = youtube_service

        search_result = SearchResult(query, str(service))

        logger.debug(f"Start searching with parameters '{query}' [service: {service}] (resultUUID: {search_result.uuid})")

        found = await service.search(query=query)
        search_result.result = found

        logger.debug(f"Successfully finished searching for query '{query}' [service: {service}] (resultUUID: {search_result.uuid})")

        return search_result


class SearchManager(BaseSearchManager):
    pass


search_manager = SearchManager()
