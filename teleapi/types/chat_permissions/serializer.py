from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ChatPermissions


class ChatPermissionsSerializer(ModelSerializer):
    class Meta:
        model = ChatPermissions
