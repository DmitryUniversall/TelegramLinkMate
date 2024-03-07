from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField, ListSerializerField
from .obj import InputSticker
from teleapi.types.mask_position import MaskPositionSerializer


class InputStickerSerializer(ModelSerializer):
    emoji_list = ListSerializerField(StringSerializerField(max_size=2024), min_size=1, max_size=20, is_required=False)
    keywords = ListSerializerField(StringSerializerField(max_size=64), max_size=20, default=[], is_required=False)
    mask_position = RelatedSerializerField(MaskPositionSerializer(), is_required=False)

    class Meta:
        model = InputSticker
