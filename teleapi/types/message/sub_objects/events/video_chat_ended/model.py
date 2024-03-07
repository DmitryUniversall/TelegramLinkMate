from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField


class VideoChatEndedModel(Model):
    duration: int = IntegerModelField()
