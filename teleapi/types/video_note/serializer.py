from teleapi.types.filelike import FilelikeSerializer
from .obj import VideoNote
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.photo_size import PhotoSizeSerializer


class VideoNoteSerializer(FilelikeSerializer):
    thumbnail = RelatedSerializerField(PhotoSizeSerializer(), is_required=False)

    class Meta:
        model = VideoNote
