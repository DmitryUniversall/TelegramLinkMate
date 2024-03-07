from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import VideoChatEnded


class VideoChatEndedSerializer(ModelSerializer):
    class Meta:
        model = VideoChatEnded
