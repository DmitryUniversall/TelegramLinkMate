from .model import ChatMemberBannedModel
from teleapi.types.chat_member import ChatMember


class ChatMemberBanned(ChatMemberBannedModel, ChatMember):
    pass
