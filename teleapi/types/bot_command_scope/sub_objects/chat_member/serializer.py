from ...serializer import TelegramBotCommandScopeSerializer
from .obj import TelegramBotCommandScopeChatMember


class TelegramBotCommandScopeChatMemberSerializer(TelegramBotCommandScopeSerializer):
    class Meta:
        model = TelegramBotCommandScopeChatMember
