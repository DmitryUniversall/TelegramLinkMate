from typing import List
from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField, RelatedModelField, ListModelField
from teleapi.types.user import User


class PollAnswerModel(Model):
    poll_id: str = StringModelField()
    user: User = RelatedModelField(User)
    option_ids: List[int] = ListModelField(IntegerModelField())
