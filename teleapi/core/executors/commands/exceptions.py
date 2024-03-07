from teleapi.core.exceptions import TeleapiError


class CommandError(TeleapiError):
    default_message = "Command error"
