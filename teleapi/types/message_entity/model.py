from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, RelatedModelField
from teleapi.types.user import User


class MessageEntityModel(Model):
    type_: str = StringModelField()
    offset: int = IntegerModelField()
    length: int = IntegerModelField()
    url: Optional[str] = StringModelField(is_required=False)
    user: Optional[User] = RelatedModelField(User, is_required=False)
    language: Optional[str] = StringModelField(is_required=False)
    custom_emoji_id: Optional[str] = StringModelField(is_required=False)
