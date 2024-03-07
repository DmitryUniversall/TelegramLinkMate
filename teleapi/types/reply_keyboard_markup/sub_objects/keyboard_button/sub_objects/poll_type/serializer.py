from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import KeyboardButtonPollType


class KeyboardButtonPollTypeSerializer(ModelSerializer):
    class Meta:
        model = KeyboardButtonPollType
