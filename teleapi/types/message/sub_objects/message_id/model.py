from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField


class MessageIdModel(Model):
    message_id: int = IntegerModelField()
