from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField, IntegerModelField


class TelegramBotCommandScopeChatModel(Model):
    type_: str = ConstantModelField("chat")
    chat_id: int = IntegerModelField()  # TODO: int or str
