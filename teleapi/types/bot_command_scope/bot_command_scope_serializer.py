from typing import Any, Dict, Type
from teleapi.core.orm.serializers import Serializer
from .sub_objects.all_chat_administrator import TelegramBotCommandScopeAllChatAdministrators, \
    TelegramBotCommandScopeAllChatAdministratorsSerializer
from .sub_objects.all_group_chats import TelegramBotCommandScopeAllGroupChats, \
    TelegramBotCommandScopeAllGroupChatsSerializer
from .sub_objects.all_private_chats import TelegramBotCommandScopeAllPrivateChats, \
    TelegramBotCommandScopeAllPrivateChatsSerializer
from .sub_objects.chat import TelegramBotCommandScopeChat, TelegramBotCommandScopeChatSerializer
from .sub_objects.chat_administrators import TelegramBotCommandScopeChatAdministrators, \
    TelegramBotCommandScopeChatAdministratorsSerializer
from .sub_objects.chat_member import TelegramBotCommandScopeChatMember, TelegramBotCommandScopeChatMemberSerializer
from .sub_objects.default import TelegramBotCommandScopeDefault, TelegramBotCommandScopeDefaultSerializer
from ...core.orm.typing import JsonValue


class BotCommandScopeObjectSerializer(Serializer):
    bot_command_scope_serializers_mapping: Dict[str, Type[Serializer]] = {
        TelegramBotCommandScopeAllChatAdministrators.type_.constant: TelegramBotCommandScopeAllChatAdministratorsSerializer,
        TelegramBotCommandScopeAllGroupChats.type_.constant: TelegramBotCommandScopeAllGroupChatsSerializer,
        TelegramBotCommandScopeAllPrivateChats.type_.constant: TelegramBotCommandScopeAllPrivateChatsSerializer,
        TelegramBotCommandScopeChat.type_.constant: TelegramBotCommandScopeChatSerializer,
        TelegramBotCommandScopeChatAdministrators.type_.constant: TelegramBotCommandScopeChatAdministratorsSerializer,
        TelegramBotCommandScopeChatMember.type_.constant: TelegramBotCommandScopeChatMemberSerializer,
        TelegramBotCommandScopeDefault.type_.constant: TelegramBotCommandScopeDefaultSerializer
    }

    def to_object(self, data: JsonValue) -> Any:
        type_ = data['type']
        serializer = self.__class__.bot_command_scope_serializers_mapping.get(type_, None)

        if serializer is None:
            raise TypeError(f"Unknown BotCommandScope type_: '{type_}'")

        return serializer().to_object(data)

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        serializer = self.__class__.bot_command_scope_serializers_mapping.get(obj.type_, None)

        if serializer is None:
            raise TypeError(f"Unknown BotCommandScope type_: '{obj.type_}'")

        return serializer().to_representation(obj, keep_none_fields=keep_none_fields)
