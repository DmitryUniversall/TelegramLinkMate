from typing import Any, Dict, Type
from teleapi.core.orm.serializers import Serializer
from .sub_objects.commands import MenuButtonCommands, MenuButtonCommandsSerializer
from .sub_objects.default import MenuButtonDefault, MenuButtonDefaultSerializer
from .sub_objects.web_app import MenuButtonWebApp, MenuButtonWebAppSerializer
from ...core.orm.typing import JsonValue


class MenuButtonObjectSerializer(Serializer):
    bot_command_scope_serializers_mapping: Dict[str, Type[Serializer]] = {
        MenuButtonCommands.type_.constant: MenuButtonCommandsSerializer,
        MenuButtonDefault.type_.constant: MenuButtonDefaultSerializer,
        MenuButtonWebApp.type_.constant: MenuButtonWebAppSerializer
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
