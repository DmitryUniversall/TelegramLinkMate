from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, RelatedModelField, UnixTimestampModelField, StringModelField
from datetime import datetime
from teleapi.types.user import User
from teleapi.types.chat import Chat
from teleapi.types.chat_invite_link import ChatInviteLink
from typing import Optional


class ChatJoinRequestModel(Model):
    chat: Chat = RelatedModelField(Chat)
    user: User = RelatedModelField(User)
    user_chat_id: int = IntegerModelField()
    date: datetime = UnixTimestampModelField()
    bio: Optional[str] = StringModelField()
    invite_link: Optional[ChatInviteLink] = RelatedModelField(ChatInviteLink)
