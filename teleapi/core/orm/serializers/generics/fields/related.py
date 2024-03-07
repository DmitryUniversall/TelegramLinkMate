from teleapi.core.orm.serializers.field import SerializerField
from teleapi.core.orm.serializers.abc import Serializable
from teleapi.core.orm.typing import JsonValue
from teleapi.core.orm.validators.validator import Validator
from typing import Any, Union
from importlib import import_module


class RelatedSerializerField(Validator, SerializerField):
    def __init__(self, serializable: Union[Serializable, str], **kwargs) -> None:
        super().__init__(**kwargs)
        self._serializable = serializable

    @property
    def serializable(self) -> Serializable:
        if isinstance(self._serializable, str):
            if self._serializable == self.__owner__.__name__:
                serializable_cls = self.__owner__
            elif "." in self._serializable:
                *path, obj = self._serializable.split('.')
                module = import_module('.'.join(path))
                serializable_cls = getattr(module, obj, None)
            else:
                module = import_module(self.__owner__.__module__)
                serializable_cls = getattr(module, self._serializable, None)

            if serializable_cls is None:
                raise RuntimeError(
                    f"Cannot use it here. The specified serializer '{self._serializable}' was not found or has not been initialized yet"
                )

            self._serializable = serializable_cls()

        return self._serializable

    def to_object(self, value: JsonValue) -> Any:
        return self.serializable.to_object(value)

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        return self.serializable.to_representation(obj, keep_none_fields=keep_none_fields)
