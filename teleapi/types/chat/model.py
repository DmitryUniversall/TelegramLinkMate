from typing import Optional, List, TYPE_CHECKING
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import (
    IntegerModelField,
    StringModelField,
    BooleanModelField,
    ListModelField,
    RelatedModelField,
)
from .chat_type import ChatType
from ..chat_photo import ChatPhoto
from ..location.sub_objects.chat_location import ChatLocation
from teleapi.types.chat_permissions import ChatPermissions

if TYPE_CHECKING:
    from teleapi.types.message.obj import Message


class ChatModel(Model):
    id: int = IntegerModelField()
    type_: str = RelatedModelField(ChatType)
    is_forum: bool = BooleanModelField(is_required=False, default=False)
    has_private_forwards: bool = BooleanModelField(is_required=False, default=False)
    has_restricted_voice_and_video_messages: bool = BooleanModelField(is_required=False, default=False)
    join_to_send_messages: bool = BooleanModelField(is_required=False, default=False)
    join_by_request: bool = BooleanModelField(is_required=False, default=False)
    has_aggressive_anti_spam_enabled: bool = BooleanModelField(is_required=False, default=False)
    has_hidden_members: bool = BooleanModelField(is_required=False, default=False)
    has_protected_content: bool = BooleanModelField(is_required=False, default=False)
    can_set_sticker_set: bool = BooleanModelField(is_required=False, default=False)

    title: Optional[str] = StringModelField(is_required=False)
    username: Optional[str] = StringModelField(is_required=False)
    first_name: Optional[str] = StringModelField(is_required=False)
    last_name: Optional[str] = StringModelField(is_required=False)
    active_usernames: Optional[List[str]] = ListModelField(StringModelField(), is_required=False, default=[])
    emoji_status_custom_emoji_id: Optional[str] = StringModelField(is_required=False)
    bio: Optional[str] = StringModelField(is_required=False)
    description: Optional[str] = StringModelField(is_required=False)
    invite_link: Optional[str] = StringModelField(is_required=False)
    pinned_message: Optional['Message'] = RelatedModelField('teleapi.types.message.obj.Message', is_required=False)
    slow_mode_delay: Optional[int] = IntegerModelField(is_required=False)
    message_auto_delete_time: Optional[int] = IntegerModelField(is_required=False)
    sticker_set_name: Optional[str] = StringModelField(is_required=False)
    linked_chat_id: Optional[int] = IntegerModelField(is_required=False)

    location = RelatedModelField(ChatLocation, is_required=False)
    permissions = RelatedModelField(ChatPermissions, is_required=False)
    photo = RelatedModelField(ChatPhoto, is_required=False)
