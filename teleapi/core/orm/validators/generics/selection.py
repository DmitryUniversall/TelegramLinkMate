from teleapi.core.orm.validators.validator import Validator
from teleapi.core.orm.validators.exceptions import ValidationError
from typing import Any, List


class SelectionValidator(Validator):
    def __init__(self, variations: List[Any], **kwargs) -> None:
        super().__init__(**kwargs)
        self.variations = variations

    def validate(self, value: Any) -> Any:
        value = super().validate(value)
        if value is None:
            return

        if value not in self.variations:
            raise ValidationError(f'Value for validator {self} must be in {self.variations}')

        return value
