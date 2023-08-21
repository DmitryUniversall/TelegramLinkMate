from src.exceptions import BotError, UserError


class SearchError(BotError):
    pass


class SearchUserError(SearchError, UserError):
    pass
