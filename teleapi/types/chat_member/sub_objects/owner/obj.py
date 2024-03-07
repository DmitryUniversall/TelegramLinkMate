from .model import ChatOwnerModel
from teleapi.types.chat_member import ChatMember


class ChatOwner(ChatOwnerModel, ChatMember):
    pass
