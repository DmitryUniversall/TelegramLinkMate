from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField


class ChatSharedModel(Model):
    request_id: int = IntegerModelField()
    chat_id: int = IntegerModelField()
