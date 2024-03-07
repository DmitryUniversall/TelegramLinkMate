from .obj import ChatOwner
from teleapi.types.chat_member import ChatMemberSerializer


class ChatOwnerSerializer(ChatMemberSerializer):
    class Meta:
        model = ChatOwner
