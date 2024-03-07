from .model import ChatMemberLeftModel
from teleapi.types.chat_member import ChatMember


class ChatMemberLeft(ChatMemberLeftModel, ChatMember):
    pass
