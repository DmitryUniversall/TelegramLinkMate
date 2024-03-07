from typing import Any, Optional

from teleapi.core.orm.models.field import ModelField


class ConstantModelField(ModelField):
    def __init__(self, constant: Any, raise_exception: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.constant = constant
        self.raise_exception = raise_exception

    def __set__(self, instance: Any, value: Any) -> None:
        if self.raise_exception:
            raise AttributeError(f"Value of {self.__class__.__name__} can not be set")

    def __get__(self, instance: Optional[Any] = None, owner: Optional[type] = None) -> Any:
        if instance:
            return self.constant
        return self
