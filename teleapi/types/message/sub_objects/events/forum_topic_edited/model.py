from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField


class ForumTopicEditedModel(Model):
    name: Optional[str] = StringModelField(is_required=False)
    icon_custom_emoji_id: Optional[str] = StringModelField(is_required=False)
