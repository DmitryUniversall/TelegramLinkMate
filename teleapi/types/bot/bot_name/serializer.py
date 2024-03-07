from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import BotName


class BotNameSerializer(ModelSerializer):
    class Meta:
        model = BotName
