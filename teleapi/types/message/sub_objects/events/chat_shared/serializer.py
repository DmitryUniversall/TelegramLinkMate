from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ChatShared


class ChatSharedSerializer(ModelSerializer):
    class Meta:
        model = ChatShared
