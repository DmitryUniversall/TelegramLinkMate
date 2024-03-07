from teleapi.core.utils.collectors import CollectorMeta, collect_instances
from .field import BaseSerializerField
from typing import List, Dict, Any, Union
from .abc import Serializable
from abc import ABC, ABCMeta, abstractmethod
from teleapi.core.orm.typing import JsonValue
from .exceptions import SerializationError


class SerializerMeta(CollectorMeta, ABCMeta):
    _collector = {
        'func': collect_instances,
        'attributes': {
            BaseSerializerField: '__fields__'
        }
    }


class BaseSerializer(Serializable, metaclass=SerializerMeta):
    # Dynamic generated property that collects fields(BaseSerializerField)
    __fields__: List[BaseSerializerField]

    @abstractmethod
    def convert_to_representations(self, obj: Any, keep_none_fields: bool = True) -> Dict[JsonValue, JsonValue]:
        ...

    @abstractmethod
    def convert_to_objects(self, data: JsonValue) -> Dict[str, JsonValue]:
        ...

    def serialize(self, *, data: JsonValue = None, obj: Any = None, keep_none_fields: bool = True, many: bool = False) -> Union[List[Union[JsonValue, Any]], Union[JsonValue, Any]]:
        if data is not None:
            if many:
                return [self.to_object(element) for element in data]
            return self.to_object(data)
        elif obj is not None:
            if many:
                return [self.to_representation(element, keep_none_fields=keep_none_fields) for element in obj]
            return self.to_representation(obj, keep_none_fields=keep_none_fields)
        else:
            raise TypeError("You must define 'data' or 'obj' argument")


class Serializer(BaseSerializer, ABC):
    def convert_to_objects(self, data: JsonValue) -> Dict[str, JsonValue]:
        result = {}

        for field in filter(lambda x: not x.read_only, self.__class__.__fields__):
            value = data.get(field.read_name, None)
            validated = field.validate(value)

            if validated is None:
                result[field.__attribute_name__] = None
            else:
                result[field.__attribute_name__] = field.to_object(validated)

        return result

    def convert_to_representations(self, obj: Any, keep_none_fields: bool = True) -> Dict[JsonValue, JsonValue]:
        result = {}

        for field in filter(lambda x: not x.read_only, self.__class__.__fields__):
            value = getattr(obj, field.__attribute_name__, None)  # getattr(obj, field.name, ->None<-) - ignore error

            if value is None:
                if not keep_none_fields:
                    continue
                elif not field.is_required:
                    result[field.read_name] = None
                    continue
                else:
                    raise SerializationError(f"Field {field} is required, but its missed")

            representation = field.to_representation(value, keep_none_fields=keep_none_fields)

            if keep_none_fields or representation is not None:
                result[field.read_name] = representation

        return result

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        return self.convert_to_representations(obj, keep_none_fields=keep_none_fields)
