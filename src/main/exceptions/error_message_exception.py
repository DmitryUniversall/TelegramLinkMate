from typing import ClassVar, Optional

from src.core.exceptions import BaseBotError


class ErrorMessageException(BaseBotError):
    default_message: ClassVar[str] = "Unknown error occurred"


class NonLocalizedErrorMessageException(ErrorMessageException):
    def __init__(self, message: Optional[str] = None, **kwargs) -> None:
        super().__init__(message)

        self.kwargs = kwargs
