from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.filelike import FilelikeSerializer
from teleapi.types.photo_size import PhotoSizeSerializer
from .obj import Video


class VideoSerializer(FilelikeSerializer):
    thumbnail = RelatedSerializerField(PhotoSizeSerializer(), is_required=False)

    class Meta:
        model = Video
