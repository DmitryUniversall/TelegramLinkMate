from teleapi.core.orm.models.generics.fields import ConstantModelField
from teleapi.types.chat_member import ChatMemberModel


class ChatMemberLeftModel(ChatMemberModel):
    status: str = ConstantModelField("left")
