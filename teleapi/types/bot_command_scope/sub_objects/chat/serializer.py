from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeChat


class TelegramBotCommandScopeChatSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeChat
