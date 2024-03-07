from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField


class MessageAutoDeleteTimerChangedModel(Model):
    message_auto_delete_time: int = IntegerModelField()
