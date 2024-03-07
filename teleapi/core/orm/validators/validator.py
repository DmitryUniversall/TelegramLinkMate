from .abc import Validateable
from abc import ABC
from typing import Any, Callable, Optional
from .exceptions import ValidationError


class BaseValidator(Validateable, ABC):
    def __init__(self, is_required: bool = True, default: Any = None, validate: Callable[['BaseValidator', Any], bool] = None) -> None:
        self.is_required = is_required
        self.default = default
        self.additional_validator = validate

    def validate(self, value: Any) -> Any:
        if value is None and self.default is not None:
            value = self.default
        if value is None and not self.is_required:
            return None
        if value is None and self.is_required:
            raise ValidationError(
                f"Value of Validator {self} is missed"
            )

        if self.additional_validator is not None and not self.additional_validator(self, value):
            raise ValidationError(
                f"Additional validation failed for {self}"
            )

        return value


class Validator(BaseValidator):
    pass
