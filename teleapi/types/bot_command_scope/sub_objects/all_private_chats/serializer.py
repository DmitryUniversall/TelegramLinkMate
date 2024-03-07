from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeAllPrivateChats


class TelegramBotCommandScopeAllPrivateChatsSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeAllPrivateChats
