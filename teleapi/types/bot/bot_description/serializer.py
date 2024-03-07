from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import BotDescription


class BotDescriptionSerializer(ModelSerializer):
    class Meta:
        model = BotDescription
