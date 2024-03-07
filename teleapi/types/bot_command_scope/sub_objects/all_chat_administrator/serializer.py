from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeAllChatAdministrators


class TelegramBotCommandScopeAllChatAdministratorsSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeAllChatAdministrators
