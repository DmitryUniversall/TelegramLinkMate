from typing import Any, Sized
from teleapi.core.orm.validators.exceptions import ValidationError
from teleapi.core.orm.validators.validator import Validator


class SizedValidator(Validator):
    def __init__(self, min_size: int = None, max_size: int = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if min_size is not None and (not isinstance(min_size, int) or min_size <= 0):
            raise TypeError('min_length must be a positive integer')
        elif max_size is not None and (not isinstance(max_size, int) or max_size <= 0):
            raise TypeError('max_length must be a positive integer')
        elif (min_size is not None and max_size is not None) and max_size < min_size:
            raise ValueError('min_length must be less then max_length')

        self.min_length = min_size
        self.max_length = max_size

    def validate(self, value: Sized) -> Any:
        value = super().validate(value)

        if value is None:
            return None

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(f'Value length for validator {self} must be greater than {self.min_length}')
        elif self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(f'Value length for validator {self} must be less than {self.max_length}')

        return value
