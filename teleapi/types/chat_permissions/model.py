from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import BooleanModelField


class ChatPermissionsModel(Model):
    can_send_messages: bool = BooleanModelField(default=False)
    can_send_audios: bool = BooleanModelField(default=False)
    can_send_documents: bool = BooleanModelField(default=False)
    can_send_photos: bool = BooleanModelField(default=False)
    can_send_videos: bool = BooleanModelField(default=False)
    can_send_video_notes: bool = BooleanModelField(default=False)
    can_send_voice_notes: bool = BooleanModelField(default=False)
    can_send_polls: bool = BooleanModelField(default=False)
    can_send_other_messages: bool = BooleanModelField(default=False)
    can_add_web_page_previews: bool = BooleanModelField(default=False)
    can_change_info: bool = BooleanModelField(default=False)
    can_invite_users: bool = BooleanModelField(default=False)
    can_pin_messages: bool = BooleanModelField(default=False)
    can_manage_topics: bool = BooleanModelField(default=False)
