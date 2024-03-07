from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import MessageId


class MessageIdSerializer(ModelSerializer):
    class Meta:
        model = MessageId
