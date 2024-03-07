from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField


class ForumTopicCreatedModel(Model):
    name: str = StringModelField()
    icon_color: int = IntegerModelField()  # TODO: Отдельный класс (Color of the topic icon in RGB format)
    icon_custom_emoji_id: Optional[str] = StringModelField(is_required=False)
