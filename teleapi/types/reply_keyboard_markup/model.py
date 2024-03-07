from typing import Optional, List

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import (
    StringModelField,
    BooleanModelField,
    RelatedModelField,
    ListModelField
)

from .sub_objects.keyboard_button.obj import KeyboardButton


class ReplyKeyboardMarkupModel(Model):
    keyboard: List[List[KeyboardButton]] = ListModelField(ListModelField(RelatedModelField(KeyboardButton)))
    input_field_placeholder: Optional[str] = StringModelField(is_required=False)
    is_persistent: bool = BooleanModelField(default=False)
    resize_keyboard: bool = BooleanModelField(default=False)
    one_time_keyboard: bool = BooleanModelField(default=False)
    selective: Optional[bool] = BooleanModelField(is_required=False)
