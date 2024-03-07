from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField, ConstantModelField
from teleapi.types.chat_member import ChatMemberModel
from typing import Optional


class ChatOwnerModel(ChatMemberModel):
    status: str = ConstantModelField("creator")
    is_anonymous: bool = BooleanModelField(default=False)
    custom_title: Optional[str] = StringModelField(is_required=False)
