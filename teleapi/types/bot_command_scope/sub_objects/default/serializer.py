from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeDefault


class TelegramBotCommandScopeDefaultSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeDefault
