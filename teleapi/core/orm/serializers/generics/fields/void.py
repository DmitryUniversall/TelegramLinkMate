from typing import Any

from teleapi.core.orm import JsonValue
from teleapi.core.orm.serializers.field import SerializerField


class VoidSerializerField(SerializerField):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.is_required = False

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        return None

    def to_object(self, data: JsonValue) -> Any:
        return None
