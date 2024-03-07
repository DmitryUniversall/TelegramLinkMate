from teleapi.core.exceptions import TeleapiError


class PollError(TeleapiError):
    pass


class BadPollState(PollError):
    pass
