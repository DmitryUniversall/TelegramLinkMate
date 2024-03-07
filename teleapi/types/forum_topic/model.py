from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, RelatedModelField, IntegerModelField
from .icon_color import ForumTopicIconRGBColor


class ForumTopicModel(Model):
    message_thread_id: int = IntegerModelField()
    name: str = StringModelField()
    icon_color: int = RelatedModelField(ForumTopicIconRGBColor)
    icon_custom_emoji_id: Optional[str] = StringModelField(is_required=False)
