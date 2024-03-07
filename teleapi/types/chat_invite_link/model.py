from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, RelatedModelField, \
    BooleanModelField, UnixTimestampModelField
from teleapi.types.user import User
from typing import Optional
from datetime import datetime


class ChatInviteLinkModel(Model):
    invite_link: str = StringModelField()
    creator: User = RelatedModelField(User)
    creates_join_request: bool = BooleanModelField(default=False)
    is_primary: bool = BooleanModelField(default=False)
    is_revoked: bool = BooleanModelField(default=False)
    name: Optional[str] = StringModelField(is_required=False)
    expire_date: Optional[datetime] = UnixTimestampModelField(is_required=False)
    member_limit: Optional[int] = IntegerModelField(is_required=False)
    pending_join_request_count: Optional[int] = IntegerModelField(is_required=False)
