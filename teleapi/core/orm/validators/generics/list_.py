from teleapi.core.orm.validators.abc import Validateable
from teleapi.core.orm.typing import JsonValue
from .sized import SizedValidator
from teleapi.core.orm.validators import ValidationError


class ListValidator(SizedValidator):
    def __init__(self, validator: 'Validateable', **kwargs) -> None:
        super().__init__(**kwargs)
        self.validator = validator

    def validate(self, value: JsonValue) -> JsonValue:
        value = super().validate(value)
        if value is None:
            return

        try:
            return [self.validator.validate(element) for element in value]
        except ValidationError as error:
            raise ValidationError(f"One of list elements of {self} has not passed validation: {error}") from error
