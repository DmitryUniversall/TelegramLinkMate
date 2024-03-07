from teleapi.types.filelike import FilelikeSerializer
from .obj import PhotoSize


class PhotoSizeSerializer(FilelikeSerializer):
    class Meta:
        model = PhotoSize
