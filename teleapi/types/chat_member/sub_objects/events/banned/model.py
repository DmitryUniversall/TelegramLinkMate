from teleapi.core.orm.models.generics.fields import ConstantModelField, UnixTimestampModelField
from teleapi.types.chat_member import ChatMemberModel
from datetime import datetime


class ChatMemberBannedModel(ChatMemberModel):
    status: str = ConstantModelField("kicked")
    until_date: datetime = UnixTimestampModelField()
