from teleapi.core.orm.serializers.generics.fields import (
    IntegerSerializerField,
    RelatedSerializerField,
    ListSerializerField
)
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.types.chat.serializer import ChatSerializer
from teleapi.types.user.serializer import UserSerializer
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkupSerializer
from .obj import Message
from teleapi.types.message_entity import MessageEntitySerializer
from .sub_objects.events.chat_shared import ChatSharedSerializer
from .sub_objects.events.forum_topic_closed.serializer import ForumTopicClosedSerializer
from .sub_objects.events.forum_topic_created import ForumTopicCreatedSerializer
from .sub_objects.events.forum_topic_edited import ForumTopicEditedSerializer
from .sub_objects.events.forum_topic_reopened import ForumTopicReopenedSerializer
from .sub_objects.events.general_forum_topic_hidden import GeneralForumTopicHiddenSerializer
from .sub_objects.events.general_forum_topic_unhidden import GeneralForumTopicUnhiddenSerializer
from .sub_objects.events.message_auto_delete_timer_changed import MessageAutoDeleteTimerChangedSerializer
from .sub_objects.events.proximity_alert_triggered import ProximityAlertTriggeredSerializer
from .sub_objects.events.user_shared.serializer import UserSharedSerializer
from .sub_objects.events.video_chat_ended import VideoChatEndedSerializer
from .sub_objects.events.video_chat_participants_invited import VideoChatParticipantsInvitedSerializer
from .sub_objects.events.video_chat_scheduled import VideoChatScheduledSerializer
from .sub_objects.events.video_chat_started import VideoChatStartedSerializer
from .sub_objects.events.write_access_allowed import WriteAccessAllowedSerializer
from ..animation.serializer import AnimationSerializer
from ..audio.serializer import AudioSerializer
from ..contact import ContactSerializer
from ..dice import DiceSerializer
from ..document import DocumentSerializer
from ..location import LocationSerializer
from ..photo_size.serializer import PhotoSizeSerializer
from ..poll import PollSerializer
from ..story import StorySerializer
from ..venue import VenueSerializer
from ..video.serializer import VideoSerializer
from ..video_note import VideoNoteSerializer
from ..voice.serializer import VoiceSerializer


class MessageSerializer(ModelSerializer):
    id = IntegerSerializerField(read_name="message_id")
    author = RelatedSerializerField(UserSerializer(), read_name="from", is_required=False)
    chat = RelatedSerializerField(ChatSerializer())
    thread_id = IntegerSerializerField(read_name="message_thread_id", is_required=False)
    sender_chat = RelatedSerializerField(ChatSerializer(), is_required=False)
    via_bot = RelatedSerializerField(UserSerializer(), is_required=False)
    reply_markup = RelatedSerializerField(InlineKeyboardMarkupSerializer(), is_required=False)
    forward_from = RelatedSerializerField(UserSerializer(), is_required=False)
    forward_from_chat = RelatedSerializerField(ChatSerializer(), is_required=False)
    reply_to_message = RelatedSerializerField('MessageSerializer', is_required=False)
    pinned_message = RelatedSerializerField('MessageSerializer', is_required=False)
    entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    caption_entities = ListSerializerField(RelatedSerializerField(MessageEntitySerializer()), is_required=False)
    photo = ListSerializerField(RelatedSerializerField(PhotoSizeSerializer()), is_required=False)
    animation = RelatedSerializerField(AnimationSerializer(), is_required=False)
    audio = RelatedSerializerField(AudioSerializer(), is_required=False)
    document = RelatedSerializerField(DocumentSerializer(), is_required=False)
    video = RelatedSerializerField(VideoSerializer(), is_required=False)
    video_note = RelatedSerializerField(VideoNoteSerializer(), is_required=False)
    voice = RelatedSerializerField(VoiceSerializer(), is_required=False)
    new_chat_photo = ListSerializerField(RelatedSerializerField(PhotoSizeSerializer()), is_required=False)
    new_chat_members = ListSerializerField(RelatedSerializerField(UserSerializer()), is_required=False)
    left_chat_member = RelatedSerializerField(UserSerializer(), is_required=False)
    contact = RelatedSerializerField(ContactSerializer(), is_required=False)
    poll = RelatedSerializerField(PollSerializer(), is_required=False)
    dice = RelatedSerializerField(DiceSerializer(), is_required=False)
    story = RelatedSerializerField(StorySerializer(), is_required=False)
    location = RelatedSerializerField(LocationSerializer(), is_required=False)
    venue = RelatedSerializerField(VenueSerializer(), is_required=False)
    message_auto_delete_timer_changed = RelatedSerializerField(MessageAutoDeleteTimerChangedSerializer(), is_required=False)
    video_chat_scheduled = RelatedSerializerField(VideoChatScheduledSerializer(), is_required=False)
    video_chat_started = RelatedSerializerField(VideoChatStartedSerializer(), is_required=False)
    video_chat_ended = RelatedSerializerField(VideoChatEndedSerializer(), is_required=False)
    video_chat_participants_invited = RelatedSerializerField(VideoChatParticipantsInvitedSerializer(), is_required=False)
    user_shared = RelatedSerializerField(UserSharedSerializer(), is_required=False)
    chat_shared = RelatedSerializerField(ChatSharedSerializer(), is_required=False)
    forum_topic_created = RelatedSerializerField(ForumTopicCreatedSerializer(), is_required=False)
    forum_topic_edited = RelatedSerializerField(ForumTopicEditedSerializer(), is_required=False)
    forum_topic_closed = RelatedSerializerField(ForumTopicClosedSerializer(), is_required=False)
    forum_topic_reopened = RelatedSerializerField(ForumTopicReopenedSerializer(), is_required=False)
    general_forum_topic_hidden = RelatedSerializerField(GeneralForumTopicHiddenSerializer(), is_required=False)
    general_forum_topic_unhidden = RelatedSerializerField(GeneralForumTopicUnhiddenSerializer(), is_required=False)
    write_access_allowed = RelatedSerializerField(WriteAccessAllowedSerializer(), is_required=False)
    proximity_alert_triggered = RelatedSerializerField(ProximityAlertTriggeredSerializer(), is_required=False)

    class Meta:
        model = Message
