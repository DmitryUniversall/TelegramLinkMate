from teleapi.core.orm.validators.generics.list_ import ListValidator
from .related import RelatedSerializerField
from teleapi.core.orm.typing import JsonValue
from typing import Any, Union
from teleapi.core.orm.serializers.abc import Serializable


class ListSerializerField(RelatedSerializerField, ListValidator):
    def __init__(self, serializable: Union[Serializable, str], **kwargs) -> None:
        super().__init__(**kwargs, serializable=serializable, validator=serializable)

    def to_object(self, value: JsonValue) -> Any:
        return [self.serializable.to_object(element) for element in value]

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        return [self.serializable.to_representation(element, keep_none_fields=keep_none_fields) for element in obj]
