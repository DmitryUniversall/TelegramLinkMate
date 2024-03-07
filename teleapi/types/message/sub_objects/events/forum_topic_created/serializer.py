from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ForumTopicCreated


class ForumTopicCreatedSerializer(ModelSerializer):
    class Meta:
        model = ForumTopicCreated
