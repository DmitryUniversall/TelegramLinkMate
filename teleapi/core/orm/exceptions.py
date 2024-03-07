from teleapi.core.exceptions.teleapi import TeleapiError


class OrmError(TeleapiError):
    default_message = 'Orm error'
