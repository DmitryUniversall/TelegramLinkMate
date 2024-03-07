from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import BooleanModelField


class ReplyKeyboardRemoveModel(Model):
    remove_keyboard: bool = BooleanModelField(is_required=False, default=True)
    selective: Optional[bool] = BooleanModelField(is_required=False)
