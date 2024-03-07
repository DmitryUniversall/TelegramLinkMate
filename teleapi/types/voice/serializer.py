from teleapi.types.filelike import FilelikeSerializer
from .obj import Voice


class VoiceSerializer(FilelikeSerializer):
    class Meta:
        model = Voice
