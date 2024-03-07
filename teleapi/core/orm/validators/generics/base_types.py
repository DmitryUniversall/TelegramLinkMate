from typing import Any, Union

from .typed import TypedValidator
from .sized import SizedValidator
from teleapi.core.orm.validators.exceptions import ValidationError
from datetime import datetime


class BooleanValidator(TypedValidator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, type_=bool)


class IntegerValidator(TypedValidator):
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs) -> None:
        super().__init__(**kwargs, type_=int)
        if min_value is not None and not isinstance(min_value, int):
            raise TypeError(f'min_value must be of type int; got {type(min_value)}')
        elif max_value is not None and not isinstance(max_value, int):
            raise TypeError(f'max_value must be of type int; got {type(min_value)}')
        elif (min_value is not None and max_value is not None) and max_value < min_value:
            raise ValueError('min_value must be less then max_length')

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> Any:
        value = super().validate(value)

        if value is None:
            return None

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f'Value of validator {self} must be greater than {self.min_value}')
        elif self.max_value is not None and value > self.max_value:
            raise ValidationError(f'Value of validator {self} must be less than {self.max_value}')

        return value


class FloatValidator(TypedValidator):
    def __init__(self, min_value: Union[float, int] = None, max_value: Union[float, int] = None, **kwargs) -> None:
        super().__init__(**kwargs, type_=float)
        if min_value is not None and not isinstance(min_value, (int, float)):
            raise TypeError(f'min_value must be of type float or int; got {type(min_value)}')
        elif max_value is not None and not isinstance(max_value, (int, float)):
            raise TypeError(f'max_value must be of type float or int; got {type(min_value)}')
        elif (min_value is not None and max_value is not None) and max_value < min_value:
            raise ValueError('min_value must be less then max_length')

        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> Any:
        value = super().validate(value)

        if value is None:
            return None

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f'Value of validator {self} must be greater than {self.min_value}')
        elif self.max_value is not None and value > self.max_value:
            raise ValidationError(f'Value of validator {self} must be less than {self.max_value}')

        return value


class StringValidator(TypedValidator, SizedValidator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, type_=str)


class DatetimeValidator(TypedValidator):  # TODO: min, max datetime
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, type_=datetime)
