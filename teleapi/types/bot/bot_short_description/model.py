from teleapi.core.orm.models.generics.fields import StringModelField
from teleapi.core.orm.models import Model


class BotShortDescriptionModel(Model):
    short_description: str = StringModelField()
