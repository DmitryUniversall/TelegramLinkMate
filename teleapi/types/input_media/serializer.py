from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField, \
    ListSerializerField, EnumSerializerField, VoidSerializerField
from .obj import InputMedia
from ..message_entity import MessageEntitySerializer
from teleapi.enums.parse_mode import ParseMode


class InputMediaSerializer(ModelSerializer):  # TODO: Наследоваться от InputFileSerializer?
    type_ = StringSerializerField(read_name='type')
    caption_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    parse_mode = EnumSerializerField(ParseMode, StringSerializerField(), default=ParseMode.NONE)

    data = VoidSerializerField()
    filename = VoidSerializerField()
    thumbnail_data = VoidSerializerField()

    class Meta:
        model = InputMedia
