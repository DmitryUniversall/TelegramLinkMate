from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import CallbackGame


class CallbackGameSerializer(ModelSerializer):
    class Meta:
        model = CallbackGame
