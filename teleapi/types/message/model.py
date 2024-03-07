from typing import TYPE_CHECKING, Optional, List

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import (
    IntegerModelField,
    StringModelField,
    BooleanModelField,
    RelatedModelField,
    UnixTimestampModelField, ListModelField
)
from teleapi.types.chat.obj import Chat
from teleapi.types.user.obj import User
from .sub_objects.events.chat_shared import ChatShared
from .sub_objects.events.forum_topic_closed.obj import ForumTopicClosed
from .sub_objects.events.forum_topic_created import ForumTopicCreated
from .sub_objects.events.forum_topic_edited import ForumTopicEdited
from .sub_objects.events.forum_topic_reopened import ForumTopicReopened
from .sub_objects.events.general_forum_topic_hidden import GeneralForumTopicHidden
from .sub_objects.events.general_forum_topic_unhidden import GeneralForumTopicUnhidden
from .sub_objects.events.message_auto_delete_timer_changed import MessageAutoDeleteTimerChanged
from .sub_objects.events.proximity_alert_triggered import ProximityAlertTriggered
from .sub_objects.events.user_shared import UserShared
from .sub_objects.events.video_chat_ended import VideoChatEnded
from .sub_objects.events.video_chat_participants_invited import VideoChatParticipantsInvited
from .sub_objects.events.video_chat_scheduled import VideoChatScheduled
from .sub_objects.events.video_chat_started import VideoChatStarted
from .sub_objects.events.write_access_allowed import WriteAccessAllowed
from ..animation.obj import Animation
from ..audio.obj import Audio
from ..contact import Contact
from ..dice.obj import Dice
from ..document import Document
from ..inline_keyboard_markup import InlineKeyboardMarkup
from datetime import datetime

from ..location.obj import Location
from ..message_entity import MessageEntity
from ..photo_size.obj import PhotoSize
from ..poll import Poll
from ..story import Story
from ..venue import Venue
from ..video.obj import Video
from ..video_note import VideoNote
from ..voice.obj import Voice

if TYPE_CHECKING:
    from .obj import Message


class MessageModel(Model):
    """
    Represents a message sent in a chat.

    Base Info:
        :cvar id: int
            The unique identifier for this message.
        :cvar chat: Chat
            The chat to which the message belongs.
        :cvar date: datetime
            The date when the message was sent.
        :cvar has_media_spoiler: bool
            (Optional) Whether the message contains media with spoiler content.
        :cvar is_automatic_forward: bool
            (Optional) True, if the message is a channel post that was automatically forwarded to the connected discussion group
        :cvar has_protected_content: bool
            (Optional) True, if the message can't be forwarded
        :cvar is_topic_message: bool
            (Optional) True, if the message is sent to a forum topic
        :cvar author: User
            (Optional) The author of the message.
        :cvar thread_id: int
            (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only
        :cvar sender_chat: Chat
            (Optional) Sender of the message, sent on behalf of a chat.
            For example, the channel itself for channel posts, the supergroup itself for messages from anonymous group administrators,
            the linked channel for messages automatically forwarded to the discussion group.
            For backward compatibility, the field from contains a fake sender user in non-channel chats,
            if the message was sent on behalf of a chat.
        :cvar via_bot: User
            (Optional) The bot through which the message was sent.
        :cvar media_group_id: str
            (Optional) The identifier of the media group this message belongs to.
        :cvar author_signature: str
            (Optional) Signature of the post author for messages in channels, or the custom title of an anonymous group administrator
        :cvar migrate_to_chat_id: int
            (Optional) he group has been migrated to a supergroup with the specified identifier.
            This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it.
            But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        :cvar migrate_from_chat_id: int
            (Optional) The chat ID from which the chat was migrated.
        :cvar reply_to_message: Message
            (Optional) The message to which this message is a reply.
        :cvar edit_date: datetime
            (Optional) The date when the message was last edited.

    Text:
        :cvar text: str
            (Optional) The text content of the message.
        :cvar caption: str
            (Optional) The caption for the media in the message.

    Entities:
        :cvar entities: List[MessageEntity]
            (Optional) List of message entities in the message text.
        :cvar caption_entities: List[MessageEntity]
            (Optional) List of message entities in the caption.

    Media:
        :cvar photo: List[PhotoSize]
            (Optional) Available sizes of the photo
        :cvar animation: Animation
            (Optional) Information about the animation.
            For backward compatibility, when this field is set, the document field will also be set
        :cvar audio: Audio
            (Optional) Information about the audio
        :cvar document: Document
            (Optional) Information about the document
        :cvar video: Video
            (Optional) Information about the video
        :cvar video_note: VideoNote
            (Optional) Information about the video message

    UI:
        :cvar reply_markup: InlineKeyboardMarkup
            (Optional) Inline keyboard markup for the message. (Buttons)

    Origin:
        :cvar forward_from: User
            (Optional) Sender of the original message
        :cvar forward_from_chat: Chat
            (Optional) The chat from which the message was forwarded.
        :cvar forward_from_message_id: int
            (Optional) Identifier of the original message in the channel
        :cvar forward_signature: str
            (Optional) For forwarded messages that were originally sent in channels or by an anonymous chat administrator, signature of the message sender if present
        :cvar forward_sender_name: str
            (Optional) Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages

    Events:
        :cvar new_chat_title: str
            (Optional) Service message: A chat title was changed to this value
        :cvar delete_chat_photo: bool
            (Optional) Service message: the chat photo was deleted
        :cvar group_chat_created: bool
            (Optional) Service message: the group has been created
        :cvar supergroup_chat_created: bool
            (Optional) Service message: the supergroup has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created.
            It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        :cvar channel_chat_created: bool
            (Optional) Service message: the channel has been created.
            This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created.
            It can only be found in reply_to_message if someone replies to a very first message in a channel.
        :cvar new_chat_photo: List[PhotoSize]
            (Optional) A chat photo was change to this value
        :cvar new_chat_members: List[User]
            (Optional) New members that were added to the group or supergroup and information about them
            (the bot itself may be one of these members)
        :cvar left_chat_member: User
            (Optional) A member was removed from the group, information about them
            (the bot itself may be one of these members)

        TODO: OTHER FIELDS
    """

    # Base data
    id: int = IntegerModelField()
    chat: Chat = RelatedModelField(Chat)
    date: datetime = UnixTimestampModelField()
    has_media_spoiler: bool = BooleanModelField(is_required=False, default=False)
    is_automatic_forward: bool = BooleanModelField(is_required=False, default=False)
    has_protected_content: bool = BooleanModelField(is_required=False, default=False)
    is_topic_message: bool = BooleanModelField(is_required=False, default=False)
    author: Optional[User] = RelatedModelField(User, is_required=False)
    thread_id: Optional[int] = IntegerModelField(is_required=False)
    sender_chat: Optional[Chat] = RelatedModelField(Chat, is_required=False)
    via_bot: Optional[User] = RelatedModelField(User, is_required=False)
    media_group_id: Optional[str] = StringModelField(is_required=False)
    author_signature: Optional[str] = StringModelField(is_required=False)
    migrate_to_chat_id: Optional[int] = IntegerModelField(is_required=False)
    migrate_from_chat_id: Optional[int] = IntegerModelField(is_required=False)
    reply_to_message: Optional['Message'] = RelatedModelField('teleapi.types.message.obj.Message', is_required=False)
    edit_date: Optional[datetime] = UnixTimestampModelField(is_required=False)

    # Text
    text: Optional[str] = StringModelField(is_required=False)
    caption: Optional[str] = StringModelField(is_required=False)

    # Entities
    entities: Optional[List[MessageEntity]] = ListModelField(RelatedModelField(MessageEntity), is_required=False)
    caption_entities: Optional[List[MessageEntity]] = ListModelField(RelatedModelField(MessageEntity), is_required=False)

    # Media
    photo: Optional[List[PhotoSize]] = ListModelField(RelatedModelField(PhotoSize), is_required=False)
    animation: Optional[Animation] = RelatedModelField(Animation, is_required=False)
    audio: Optional[Audio] = RelatedModelField(Audio, is_required=False)
    document: Optional[Document] = RelatedModelField(Document, is_required=False)
    video: Optional[Video] = RelatedModelField(Video, is_required=False)
    video_note: Optional[VideoNote] = RelatedModelField(VideoNote, is_required=False)
    voice: Optional[Voice] = RelatedModelField(Voice, is_required=False)
    contact: Optional[Contact] = RelatedModelField(Contact, is_required=False)
    poll: Optional[Poll] = RelatedModelField(Poll, is_required=False)
    dice: Optional[Dice] = RelatedModelField(Dice, is_required=False)
    location: Optional[Location] = RelatedModelField(Location, is_required=False)
    venue: Optional[Venue] = RelatedModelField(Venue, is_required=False)
    story: Optional[Story] = RelatedModelField(Story, is_required=False)
    # sticker: Optional[sticker] = RelatedModelField(sticker, is_required=False)
    # game: Optional[Game] = RelatedModelField(Game, is_required=False)
    # web_app_data: Optional[WebAppData] = RelatedModelField(WebAppData, is_required=False)

    # Ui
    reply_markup: Optional[InlineKeyboardMarkup] = RelatedModelField(InlineKeyboardMarkup, is_required=False)

    # Origin
    forward_from: Optional[User] = RelatedModelField(User, is_required=False)
    forward_from_chat: Optional[Chat] = RelatedModelField(Chat, is_required=False)
    forward_from_message_id: Optional[int] = IntegerModelField(is_required=False)
    forward_signature: Optional[str] = StringModelField(is_required=False)
    forward_sender_name: Optional[str] = StringModelField(is_required=False)

    # Events (Service messages)
    new_chat_title: Optional[str] = StringModelField(is_required=False)
    delete_chat_photo: bool = BooleanModelField(is_required=False, default=False)
    group_chat_created: bool = BooleanModelField(is_required=False, default=False)
    supergroup_chat_created: bool = BooleanModelField(is_required=False, default=False)
    channel_chat_created: bool = BooleanModelField(is_required=False, default=False)
    connected_website: Optional[str] = StringModelField(is_required=False)
    pinned_message: Optional['Message'] = RelatedModelField('teleapi.types.message.obj.Message', is_required=False)
    new_chat_photo: Optional[List[PhotoSize]] = ListModelField(RelatedModelField(PhotoSize), is_required=False)
    new_chat_members: Optional[List[User]] = ListModelField(RelatedModelField(User), is_required=False)
    left_chat_member: Optional[User] = RelatedModelField(User, is_required=False)
    message_auto_delete_timer_changed: Optional[MessageAutoDeleteTimerChanged] = RelatedModelField(MessageAutoDeleteTimerChanged, is_required=False)
    video_chat_scheduled: Optional[VideoChatScheduled] = RelatedModelField(VideoChatScheduled, is_required=False)
    video_chat_started: Optional[VideoChatStarted] = RelatedModelField(VideoChatStarted, is_required=False)
    video_chat_ended: Optional[VideoChatEnded] = RelatedModelField(VideoChatEnded, is_required=False)
    video_chat_participants_invited: Optional[VideoChatParticipantsInvited] = RelatedModelField(VideoChatParticipantsInvited, is_required=False)
    user_shared: Optional[UserShared] = RelatedModelField(UserShared, is_required=False)
    chat_shared: Optional[ChatShared] = RelatedModelField(ChatShared, is_required=False)

    write_access_allowed: Optional[WriteAccessAllowed] = RelatedModelField(WriteAccessAllowed, is_required=False)
    proximity_alert_triggered: Optional[ProximityAlertTriggered] = RelatedModelField(ProximityAlertTriggered, is_required=False)

    # forum group
    forum_topic_created: Optional[ForumTopicCreated] = RelatedModelField(ForumTopicCreated, is_required=False)
    forum_topic_edited: Optional[ForumTopicEdited] = RelatedModelField(ForumTopicEdited, is_required=False)
    forum_topic_closed: Optional[ForumTopicClosed] = RelatedModelField(ForumTopicClosed, is_required=False)
    forum_topic_reopened: Optional[ForumTopicReopened] = RelatedModelField(ForumTopicReopened, is_required=False)
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = RelatedModelField(GeneralForumTopicHidden, is_required=False)
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = RelatedModelField(GeneralForumTopicUnhidden, is_required=False)

    # Payment
    # successful_payment: Optional[SuccessfulPayment] = RelatedModelField(SuccessfulPayment, is_required=False)
    # invoice: Optional[Invoice] = RelatedModelField(Invoice, is_required=False)  # Payment

    # Other
    # passport_data: Optional[PassportData] = RelatedModelField(PassportData, is_required=False)
