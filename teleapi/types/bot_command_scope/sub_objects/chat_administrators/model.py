from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField, IntegerModelField


class TelegramBotCommandScopeChatAdministratorsModel(Model):
    type_: str = ConstantModelField("chat_administrators")
    chat_id: int = IntegerModelField()  # TODO: int or str
