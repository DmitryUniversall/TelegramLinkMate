from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ForumTopicClosed


class ForumTopicClosedSerializer(ModelSerializer):
    class Meta:
        model = ForumTopicClosed
