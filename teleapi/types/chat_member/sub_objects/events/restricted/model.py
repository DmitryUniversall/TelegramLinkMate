from datetime import datetime

from teleapi.core.orm.models.generics.fields import BooleanModelField, ConstantModelField, \
    UnixTimestampModelField
from teleapi.types.chat_member import ChatMemberModel
from teleapi.types.chat_permissions import ChatPermissionsModel


class ChatMemberRestrictedModel(ChatMemberModel, ChatPermissionsModel):
    status: str = ConstantModelField("restricted")
    is_member: bool = BooleanModelField(default=False)
    until_date: datetime = UnixTimestampModelField()
