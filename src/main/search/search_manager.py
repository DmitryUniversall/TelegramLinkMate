from abc import ABC, abstractmethod
from typing import List, Optional
from .search_result import SearchResult
from .services.service import BaseService


class BaseSearchManager(ABC):
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
                return result

    @abstractmethod
    async def find(self, query: str, service: str = None) -> SearchResult:
        pass

    async def search(self, query: str, service: BaseService, use_cache: bool = True) -> Optional[SearchResult]:
        if use_cache and (result := self.find_cached(query, str(service))):
            return result

        # logger.debug(f"Start searching with parameters '{result.search_params}' (resultUUID: {result.uuid})")

        found = await service.search(query=query)
        search_result = SearchResult(query, str(service))
        search_result.result = found

        # logger.debug(f"Successfully finished searching for query '{query}'. {len(result.results)} results was found (resultUUID: {result.uuid})")

        return search_result




class SearchManager:
    def __init__(self, max_cache_size: int = 50) -> None:
        self.max_cache_size = max_cache_size
        self.__cache = {}
    async def _search(self, query: str, service: str = None) -> SearchResult:
        if service is None:
            if "music.yandex.ru" in query:
                service = YandexMusicService
            else:
                service = YoutubeService

        result = SearchResult(
            search_params=SearchParams(
                query=query,
                other_params=(
                    ('service', service),
                )
            ))

        logger.debug(f"Start searching with parameters '{result.search_params}' (resultUUID: {result.uuid})")

        service_search_manager = self.AVAILABLE_SERVICES.get(service, None)
        if service_search_manager is None:
            raise SearchFailedErrorNotification('Неизвестный сервис или функция ещё в разработке')

        found = await service_search_manager.search(query=query)

        if found:
            result.results.append(found)

        logger.debug(f"Successfully finished searching for query '{query}'. {len(result.results)} results was found (resultUUID: {result.uuid})")

        return result

    async def search(self, query: str, service: Union[str, Type[Service]] = None, use_cache: bool = True) -> SearchResult:
        if (result := self.find_cached(SearchParams(query=query, other_params=(('service', service),)))) and use_cache:
            return result
        else:
            try:
                if isinstance(service, str):
                    service_cls = services.get(service)
                    if service is None:
                        raise BotSearchError(f"Unknown service: '{service}' (type '{type(service)}')")

                    service = service_cls

                result = await self._search(
                    query=query,
                    service=service
                )
                if result:
                    self.set_cache(result)
                return result
            except BotSearchError as error:
                if not isinstance(error, NotificationException):
                    logger.warning(
                        f"An unknown error occurred while trying to search '{query}':\n{get_traceback_text(error)}"
                    )
                    raise SearchFailedErrorNotification(f"Произошла неизвестная ошибка при поиске '{query}'") from error
                raise error