from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import ConstantModelField, IntegerModelField


class TelegramBotCommandScopeChatMemberModel(Model):
    type_: str = ConstantModelField("chat_member")
    chat_id: int = IntegerModelField()  # TODO: int or str
    user_id: int = IntegerModelField()
