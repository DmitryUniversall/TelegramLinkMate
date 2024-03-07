from .obj import ChatMemberRestricted
from teleapi.types.chat_member import ChatMemberSerializer
from teleapi.types.chat_permissions import ChatPermissionsSerializer


class ChatMemberRestrictedSerializer(ChatMemberSerializer, ChatPermissionsSerializer):
    class Meta:
        model = ChatMemberRestricted
