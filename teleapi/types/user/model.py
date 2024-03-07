from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, BooleanModelField


class UserModel(Model):
    id: int = IntegerModelField()
    is_bot: bool = BooleanModelField()
    first_name: str = StringModelField()
    is_premium: bool = BooleanModelField(is_required=False, default=False)
    added_to_attachment_menu: bool = BooleanModelField(is_required=False, default=False)

    last_name: Optional[str] = StringModelField(is_required=False)
    username: Optional[str] = StringModelField(is_required=False)
    language_code: Optional[str] = StringModelField(is_required=False)
    can_join_groups: Optional[bool] = BooleanModelField(is_required=False)
    can_read_all_group_messages: Optional[bool] = BooleanModelField(is_required=False)
    supports_inline_queries: Optional[bool] = BooleanModelField(is_required=False)
