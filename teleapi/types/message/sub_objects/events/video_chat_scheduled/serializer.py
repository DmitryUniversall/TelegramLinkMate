from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import VideoChatScheduled


class VideoChatScheduledSerializer(ModelSerializer):
    class Meta:
        model = VideoChatScheduled
