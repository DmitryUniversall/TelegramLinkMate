from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, ListSerializerField, EnumSerializerField, StringSerializerField
from .obj import StickerSet
from teleapi.types.photo_size import PhotoSizeSerializer
from teleapi.types.sticker import StickerSerializer
from teleapi.types.sticker.sub_objects.sticker_type import StickerType


class StickerSetSerializer(ModelSerializer):
    sticker_type = EnumSerializerField(StickerType, StringSerializerField())
    stickers = ListSerializerField(RelatedSerializerField(StickerSerializer()))
    thumbnail = RelatedSerializerField(PhotoSizeSerializer(), is_required=False)

    class Meta:
        model = StickerSet
