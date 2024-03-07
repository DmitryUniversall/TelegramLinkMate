from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import BooleanModelField, StringModelField


class ForceReplyModel(Model):
    force_reply: bool = BooleanModelField(is_required=False, default=False)
    selective: Optional[bool] = BooleanModelField(is_required=False)
    input_field_placeholder: Optional[str] = StringModelField(is_required=False)
