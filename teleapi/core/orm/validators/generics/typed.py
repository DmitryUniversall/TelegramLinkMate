from teleapi.core.orm.validators.validator import Validator
from teleapi.core.orm.validators.exceptions import ValidationError
from importlib import import_module
from typing import Type, Any, Union, Tuple


class TypedValidator(Validator):
    def __init__(self, type_: Union[type, str, Tuple[Union[type, str,], ...]], **kwargs) -> None:
        super().__init__(**kwargs)
        self.__type = type_

    def _get_type(self, t) -> type:
        if isinstance(t, str):
            *path, obj = t.split('.')
            module = import_module('.'.join(path))
            type_ = getattr(module, obj, None)

            if type_ is None:
                raise RuntimeError(
                    f"Cannot use it here. The specified type '{t}' was not found or has not been initialized yet"
                )
            if not isinstance(type_, type):
                raise TypeError(
                    f"Specified type for {self.__class__.__name__} is not a type: {type_}"
                )
            return type_
        elif isinstance(t, type):
            return t
        else:
            raise TypeError(f"Got unknown type for {self.__class__.__name__}: {t}")

    @property
    def type_(self) -> Type[Any]:
        if isinstance(self.__type, tuple):
            self.__type = tuple(self._get_type(t) for t in self.__type)
        else:
            self.__type = self._get_type(self.__type)

        return self.__type

    def validate(self, value: Any) -> Any:
        value = super().validate(value)
        if value is None:
            return

        if not isinstance(value, self.type_):
            raise ValidationError(
                f"Value of validator {self} must be of type {self.type_}, not {type(value)} (got {value})"
            )

        return value
