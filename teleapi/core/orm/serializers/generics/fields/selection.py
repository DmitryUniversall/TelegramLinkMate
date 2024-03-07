from teleapi.core.orm.validators.generics.selection import SelectionValidator
from .related import RelatedSerializerField
from typing import Any, Union, List
from teleapi.core.orm.serializers.abc import Serializable


class SelectionSerializerField(RelatedSerializerField, SelectionValidator):
    def __init__(self, serializable: Union[Serializable, str], variations: List[Any], **kwargs) -> None:
        super().__init__(**kwargs, variations=variations, serializable=serializable)
