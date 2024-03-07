import string

from teleapi.core.orm.models.generics.fields import StringModelField
from teleapi.core.orm.models import Model


class TelegramBotCommandModel(Model):
    command: str = StringModelField(min_size=1, max_size=32, validate=lambda cmd: None if all([char in [string.ascii_lowercase + string.digits + "_"] for char in cmd]) else "TelegramBotCommandModel command field can contain only lowercase English letters, digits and underscores")
    description: str = StringModelField(min_size=1, max_size=256)
