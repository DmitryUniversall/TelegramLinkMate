from typing import List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import RelatedModelField, ListModelField
from .sub_objects.inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkupModel(Model):
    inline_keyboard: List[List[InlineKeyboardButton]] = ListModelField(ListModelField(RelatedModelField(InlineKeyboardButton)))

