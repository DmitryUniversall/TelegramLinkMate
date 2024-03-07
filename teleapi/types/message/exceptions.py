from teleapi.core.exceptions import TeleapiError


class MessageError(TeleapiError):
    pass


class MessageTooOld(MessageError):
    pass


class MessageTooNew(MessageError):
    pass


class MessageIsNotModified(MessageError):
    pass


class MessageHasNoMedia(MessageError):
    pass
