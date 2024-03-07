from datetime import datetime
from typing import Any

from teleapi.core.orm.serializers.field import SerializerField
from teleapi.core.orm.typing import JsonValue
from teleapi.core.orm.validators.generics.base_types import BooleanValidator, IntegerValidator, StringValidator, FloatValidator
from teleapi.core.orm.validators.validator import Validator


class BytesSerializerField(SerializerField, Validator):
    def to_object(self, value: JsonValue) -> Any:
        return bytes(value)

    def to_representation(self, obj: Any, **_) -> bytes:
        return bytes(obj)


class BooleanSerializerField(SerializerField, BooleanValidator):
    def to_object(self, value: JsonValue) -> Any:
        return bool(value)

    def to_representation(self, obj: Any, **_) -> JsonValue:
        return bool(obj)


class IntegerSerializerField(SerializerField, IntegerValidator):
    def to_object(self, value: JsonValue) -> Any:
        return int(value)

    def to_representation(self, obj: Any, **_) -> JsonValue:
        return int(obj)


class StringSerializerField(SerializerField, StringValidator):
    def to_object(self, value: JsonValue) -> Any:
        return str(value)

    def to_representation(self, obj: Any, **_) -> JsonValue:
        return str(obj)


class FloatSerializerField(SerializerField, FloatValidator):
    def to_object(self, value: JsonValue) -> Any:
        return float(value)

    def to_representation(self, obj: Any, **_) -> JsonValue:
        return float(obj)


class UnixTimestampSerializerField(SerializerField, IntegerValidator):
    def to_object(self, value: JsonValue) -> Any:
        return datetime.fromtimestamp(value)

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        return obj.timestamp()
