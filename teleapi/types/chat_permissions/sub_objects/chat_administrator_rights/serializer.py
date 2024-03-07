from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ChatAdministratorRights


class ChatAdministratorRightsSerializer(ModelSerializer):
    class Meta:
        model = ChatAdministratorRights
