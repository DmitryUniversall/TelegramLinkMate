from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class TelegramBotCommandScopeAllPrivateChatsModel(Model):
    type_: str = ConstantModelField("all_private_chats")
