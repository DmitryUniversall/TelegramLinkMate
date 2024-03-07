from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class TelegramBotCommandScopeAllChatAdministratorsModel(Model):
    type_: str = ConstantModelField("all_chat_administrators")
