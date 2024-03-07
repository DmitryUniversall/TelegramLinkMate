from typing import Optional


class TeleapiError(Exception):
    default_message: Optional[str] = 'Unknown error occurred'

    def __init__(self, message: str = None) -> None:
        if message is None:
            message = self.__class__.default_message

        super().__init__(message)


class CancelOperationError(TeleapiError):
    default_message = "Operation cancelled"
