from .related import RelatedSerializerField
from teleapi.core.orm.validators.generics.input_file import InputFileValidator
from teleapi.core.orm.serializers.generics.fields.base_types import BytesSerializerField


class InputFileSerializerField(RelatedSerializerField, InputFileValidator):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, serializable=BytesSerializerField())
