from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import VideoChatStarted


class VideoChatStartedSerializer(ModelSerializer):
    class Meta:
        model = VideoChatStarted
