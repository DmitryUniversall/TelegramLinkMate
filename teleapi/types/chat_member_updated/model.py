from typing import Union
from datetime import datetime

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import RelatedModelField, UnixTimestampModelField, BooleanModelField
from teleapi.types.chat import Chat
from teleapi.types.user import User
from teleapi.types.chat_member import ChatMember
from teleapi.types.chat_member.sub_objects.owner import ChatOwner
from teleapi.types.chat_member.sub_objects.administrator import ChatAdministrator
from teleapi.types.chat_member.sub_objects.events.left import ChatMemberLeft
from teleapi.types.chat_member.sub_objects.events.banned import ChatMemberBanned
from teleapi.types.chat_member.sub_objects.events.restricted import ChatMemberRestricted


class ChatMemberUpdatedModel(Model):
    chat: Chat = RelatedModelField(Chat)
    user: User = RelatedModelField(User)
    date: datetime = UnixTimestampModelField()
    old_chat_member: Union[ChatMember, ChatOwner, ChatAdministrator, ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted] = RelatedModelField((ChatMember, ChatOwner, ChatAdministrator, ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted))
    new_chat_member: Union[ChatMember, ChatOwner, ChatAdministrator, ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted] = RelatedModelField((ChatMember, ChatOwner, ChatAdministrator, ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted))
    via_chat_folder_invite_link: bool = BooleanModelField(default=False)
    # invite_link
