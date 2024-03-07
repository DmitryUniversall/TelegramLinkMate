from teleapi.core.orm.models.generics.fields import StringModelField
from teleapi.core.orm.models import Model


class BotNameModel(Model):
    name: str = StringModelField()
