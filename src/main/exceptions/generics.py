from src.core.exceptions import BaseBotError


class GenericBotError(BaseBotError):
    pass


class BadPriceError(GenericBotError):
    pass
