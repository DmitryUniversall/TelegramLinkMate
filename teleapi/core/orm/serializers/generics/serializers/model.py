import warnings
from typing import Any

from teleapi.core.orm.models import Model, ModelField
from teleapi.core.orm.models.generics.fields import *
from teleapi.core.orm.serializers import Serializer, SerializerMeta
from teleapi.core.orm.serializers.generics.fields import *
from teleapi.core.orm.typing import JsonValue


class ModelSerializerMeta(SerializerMeta):  # TODO: Переписать
    fields_mapping = {
        IntegerModelField: IntegerSerializerField,
        StringModelField: StringSerializerField,
        BooleanModelField: BooleanSerializerField,
        UnixTimestampModelField: UnixTimestampSerializerField,
        FloatModelField: FloatSerializerField
    }

    def __new__(mcs, name: str, parents: tuple, attrs: dict) -> type:
        cls = super().__new__(mcs, name, parents, attrs)

        if name == 'ModelSerializer':
            return cls

        existing_fields = getattr(cls, "__fields__", [])
        existing_field_names = [field.__attribute_name__ for field in existing_fields]

        meta = getattr(cls, "Meta", None)
        if meta is None:
            raise TypeError(f"ModelSerializer class '{cls.__name__}' missing 'Meta' attribute")

        model = getattr(meta, "model", None)
        if model is None:
            raise TypeError(f"Meta of ModelSerializer class '{cls.__name__}' missing 'model' attribute")
        if not isinstance(model, type):
            raise TypeError(f"'model' attribute of ModelSerializer Meta must type (class), not instance")
        if not issubclass(model, Model):
            raise TypeError(f"'model' attribute of ModelSerializer Meta must be subclass of 'Model'")

        model_fields = []

        if fields := getattr(meta, "fields", None):
            for field_name in fields:
                field = getattr(model, field_name, None)
                if field is None:
                    raise AttributeError(f"Model '{model}' has no field '{field_name}'")
                if not isinstance(field, ModelField):
                    raise TypeError(f"Field specified for ModelSerializer must be subclass of 'ModelField', not '{type(field)}'")

                model_fields.append(field)
        elif exclude := getattr(meta, "exclude", None):
            model_fields = [field for field in model.__fields__ if field.__attribute_name__ not in exclude]
        else:
            model_fields = model.__fields__

        enable_warnings = getattr(cls, "__enable_warnings__", True)

        for model_field in model_fields:
            if model_field.__attribute_name__ in existing_field_names:
                continue

            # noinspection PyTypeChecker
            serializer_field = mcs.fields_mapping.get(model_field.__class__)

            if not serializer_field:
                if enable_warnings:
                    warnings.warn(
                        f"Field {model_field} was declared in model, but it is not supported py ModelSerializer. Please, declare it manually")
                continue

            if not isinstance(serializer_field, type) and callable(serializer_field):
                field = serializer_field(model_field, serializer_field)
            else:
                field = serializer_field()

            field.__owner__ = cls
            field.__attribute_name__ = model_field.__attribute_name__

            field.read_name = model_field.__attribute_name__
            field.is_required = model_field.is_required
            field.default = model_field.default

            setattr(cls, field.__attribute_name__, field)

        return cls


class ModelSerializer(Serializer, metaclass=ModelSerializerMeta):
    class Meta:
        pass

    def to_object(self, value: JsonValue) -> Any:
        return self.__class__.Meta.model(**self.convert_to_objects(value))
