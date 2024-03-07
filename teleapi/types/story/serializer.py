from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Story


class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
