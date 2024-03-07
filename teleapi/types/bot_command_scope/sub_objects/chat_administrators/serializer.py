from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeChatAdministrators


class TelegramBotCommandScopeChatAdministratorsSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeChatAdministrators
