from .model import ChatMemberRestrictedModel
from teleapi.types.chat_member import ChatMember
from teleapi.types.chat_permissions import ChatPermissions


class ChatMemberRestricted(ChatMemberRestrictedModel, ChatMember, ChatPermissions):
    pass
