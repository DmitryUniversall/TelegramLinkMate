from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class TelegramBotCommandScopeDefaultModel(Model):
    type_: str = ConstantModelField("default")
