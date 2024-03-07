from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField


class TelegramBotCommandScopeAllGroupChatsModel(Model):
    type_: str = ConstantModelField("all_group_chats")
