from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ForumTopicReopened


class ForumTopicReopenedSerializer(ModelSerializer):
    class Meta:
        model = ForumTopicReopened
