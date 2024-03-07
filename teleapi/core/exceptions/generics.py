from .teleapi import TeleapiError


class FileTooLargeError(TeleapiError):
    pass


class ParameterConflictError(TeleapiError):
    pass


class InvalidParameterError(TeleapiError):
    pass
