from teleapi.core.orm.exceptions import OrmError


class ValidationError(OrmError):
    default_message = "Validation failed"
