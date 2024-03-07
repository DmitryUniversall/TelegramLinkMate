from typing import Optional
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField


class ContactModel(Model):
    phone_number: str = StringModelField()
    first_name: str = StringModelField()
    last_name: Optional[str] = StringModelField(is_required=False)
    user_id: Optional[int] = IntegerModelField(is_required=False)
    vcard: Optional[str] = StringModelField(is_required=False)
