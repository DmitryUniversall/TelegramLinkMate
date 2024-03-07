from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeAllGroupChats


class TelegramBotCommandScopeAllGroupChatsSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeAllGroupChats
