from .obj import ChatMemberBanned
from teleapi.types.chat_member import ChatMemberSerializer


class ChatMemberBannedSerializer(ChatMemberSerializer):
    class Meta:
        model = ChatMemberBanned
