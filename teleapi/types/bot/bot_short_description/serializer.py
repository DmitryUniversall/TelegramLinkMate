from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import BotShortDescription


class BotShortDescriptionSerializer(ModelSerializer):
    class Meta:
        model = BotShortDescription
