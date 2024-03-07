from src.core.exceptions import BaseBotError
from src.main.exceptions import ErrorMessageException


class SearchError(BaseBotError):
    pass


class SearchUserError(SearchError, ErrorMessageException):
    pass


class NotFoundUserError(SearchUserError):
    pass


class SearchFailedUserError(SearchUserError):
    pass
