from teleapi.types.filelike import FilelikeSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.photo_size import PhotoSizeSerializer
from .obj import Audio


class AudioSerializer(FilelikeSerializer):
    thumbnail = RelatedSerializerField(PhotoSizeSerializer(), is_required=False)

    class Meta:
        model = Audio
