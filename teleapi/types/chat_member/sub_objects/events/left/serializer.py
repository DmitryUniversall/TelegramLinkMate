from .obj import ChatMemberLeft
from teleapi.types.chat_member import ChatMemberSerializer


class ChatMemberLeftSerializer(ChatMemberSerializer):
    class Meta:
        model = ChatMemberLeft
