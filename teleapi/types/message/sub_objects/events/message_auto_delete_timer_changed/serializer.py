from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import MessageAutoDeleteTimerChanged


class MessageAutoDeleteTimerChangedSerializer(ModelSerializer):
    class Meta:
        model = MessageAutoDeleteTimerChanged
