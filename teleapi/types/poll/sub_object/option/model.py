from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, StringModelField


class PollOptionModel(Model):
    text: str = StringModelField()
    voter_count: int = IntegerModelField()

