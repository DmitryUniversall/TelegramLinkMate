from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField
from typing import Optional


class ResponseParametersModel(Model):
    migrate_to_chat_id: Optional[int] = IntegerModelField(is_required=False)
    retry_after: Optional[int] = IntegerModelField(is_required=False)
