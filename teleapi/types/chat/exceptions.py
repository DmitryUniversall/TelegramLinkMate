from teleapi.core.exceptions import TeleapiError


class ChatError(TeleapiError):
    pass


class BadChatType(ChatError):
    pass
