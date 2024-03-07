from teleapi.core.orm.serializers.generics.fields import StringSerializerField
from teleapi.types.input_media import InputMediaSerializer
from .obj import InputMediaAnimation


class InputMediaAnimationSerializer(InputMediaSerializer):
    thumbnail = StringSerializerField(is_required=False)

    class Meta:
        model = InputMediaAnimation
