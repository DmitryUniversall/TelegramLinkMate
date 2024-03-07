from abc import ABC, abstractmethod
from typing import Any
from teleapi.core.orm.typing import JsonValue


class Serializable(ABC):
    @abstractmethod
    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        pass

    @abstractmethod
    def to_object(self, data: JsonValue) -> Any:
        pass
