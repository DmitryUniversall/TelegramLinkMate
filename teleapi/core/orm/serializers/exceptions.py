from teleapi.core.orm.exceptions import OrmError


class SerializationError(OrmError):
    default_message = "SerializationError failed"
