from .abc import Serializable
from abc import ABC
from teleapi.core.orm.field_mixin import FieldMixin
from teleapi.core.orm.validators.validator import BaseValidator


class BaseSerializerField(BaseValidator, FieldMixin, Serializable, ABC):
    def __init__(self, read_name: str = None, read_only: bool = False, write_only: bool = False, **kwargs) -> None:
        super().__init__(**kwargs)
        self.read_name = read_name
        self.read_only = read_only
        self.write_only = write_only

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{self.__attribute_name__}({self.read_name}) of {self.__owner__.__name__}]>"

    def __set_name__(self, owner: type, name: str) -> None:
        super().__set_name__(owner, name)

        if self.read_name is None:
            self.read_name = name


class SerializerField(BaseSerializerField, ABC):
    pass
