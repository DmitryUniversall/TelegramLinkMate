from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, RelatedModelField, BooleanModelField
from teleapi.types.user.obj import User
from teleapi.types.message.obj import Message


class CallbackQueryModel(Model):
    id: str = StringModelField()
    user: User = RelatedModelField(User)
    chat_instance: str = StringModelField()
    message: Optional[Message] = RelatedModelField(Message, is_required=False)
    data: Optional[str] = StringModelField(is_required=False)
    game_short_name: Optional[str] = StringModelField(is_required=False)
    inline_message_id: Optional[str] = StringModelField(is_required=False)

    is_answered: bool = BooleanModelField(default=False)
