from .obj import ChatAdministrator
from teleapi.types.chat_member import ChatMemberSerializer
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRightsSerializer


class ChatAdministratorSerializer(ChatMemberSerializer, ChatAdministratorRightsSerializer):
    class Meta:
        model = ChatAdministrator
