from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import KeyboardButtonRequestUser


class KeyboardButtonRequestUserSerializer(ModelSerializer):
    class Meta:
        model = KeyboardButtonRequestUser
