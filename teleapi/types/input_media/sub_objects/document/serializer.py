from teleapi.core.orm.serializers.generics.fields import StringSerializerField
from teleapi.types.input_media import InputMediaSerializer
from .obj import InputMediaDocument


class InputMediaDocumentSerializer(InputMediaSerializer):
    thumbnail = StringSerializerField(is_required=False)

    class Meta:
        model = InputMediaDocument
