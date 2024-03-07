from .base import BaseBotError


class UnknownBotError(BaseBotError):
    """
    An exception class representing an error when encountering an unknown or unexpected issue related to a bot.
    Subclasses the BaseBotError class.

    Attributes:
    - `original`: `Exception`
        The original exception that led to the UnknownBotError.

    Methods:
    - `__init__(self, original: Exception, *args, **kwargs) -> None`
        Initializes the UnknownBotError instance.
    """

    def __init__(self, original: Exception, *args, **kwargs) -> None:
        """
        Initializes the UnknownBotError instance.

        :param original: `Exception`
            The original exception that led to the UnknownBotError.

        :param args: `Tuple`
            Additional positional arguments to be passed to parent class.

        :param kwargs: `Dict`
            Additional keyword arguments to be passed to parent class.
        """

        super().__init__(*args, **kwargs)
        self.original = original
