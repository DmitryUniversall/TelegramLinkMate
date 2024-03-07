from teleapi.types.input_media import InputMediaSerializer
from .obj import InputMediaVideo
from teleapi.core.orm.serializers.generics.fields import StringSerializerField


class InputMediaVideoSerializer(InputMediaSerializer):
    thumbnail = StringSerializerField(is_required=False)

    class Meta:
        model = InputMediaVideo
