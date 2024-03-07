from src.core.exceptions import BaseBotError


class UIError(BaseBotError):
    pass


class ViewHasNoMessageError(UIError):
    pass
