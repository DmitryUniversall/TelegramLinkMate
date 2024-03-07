from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ForumTopicEdited


class ForumTopicEditedSerializer(ModelSerializer):
    class Meta:
        model = ForumTopicEdited
