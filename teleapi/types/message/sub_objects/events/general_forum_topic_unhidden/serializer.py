from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import GeneralForumTopicUnhidden


class GeneralForumTopicUnhiddenSerializer(ModelSerializer):
    class Meta:
        model = GeneralForumTopicUnhidden
