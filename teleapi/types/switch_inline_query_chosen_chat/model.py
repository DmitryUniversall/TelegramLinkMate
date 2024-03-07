from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField


class SwitchInlineQueryChosenChatModel(Model):
    query: Optional[str] = StringModelField()
    allow_user_chats: Optional[bool] = BooleanModelField(default=False)
    allow_bot_chats: Optional[bool] = BooleanModelField(default=False)
    allow_group_chats: Optional[bool] = BooleanModelField(default=False)
    allow_channel_chats: Optional[bool] = BooleanModelField(default=False)
