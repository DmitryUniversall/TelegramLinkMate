from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import StringModelField, BooleanModelField


class LoginUrlModel(Model):
    url: str = StringModelField(validate=lambda x: None if x.startswith("https://") else "Bad WebAppInfo url (must starts with https://)")
    request_write_access: bool = BooleanModelField(default=False)
    forward_text: Optional[str] = StringModelField(is_required=False)
    bot_username: Optional[str] = StringModelField(is_required=False)
