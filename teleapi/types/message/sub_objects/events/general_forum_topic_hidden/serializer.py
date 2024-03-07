from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import GeneralForumTopicHidden


class GeneralForumTopicHiddenSerializer(ModelSerializer):
    class Meta:
        model = GeneralForumTopicHidden
