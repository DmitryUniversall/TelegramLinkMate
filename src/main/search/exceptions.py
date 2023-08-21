from src.exceptions import BotError, UserError


class SearchError(BotError):
    pass


class SearchUserError(SearchError, UserError):
    pass


class NotFoundUserError(SearchUserError):
    pass


class SearchFailedUserError(SearchUserError):
    pass
