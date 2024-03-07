from typing import Any, Dict, Type

from teleapi.core.orm.serializers import Serializer
from ...core.orm.typing import JsonValue
from .sub_objects.owner import ChatOwner, ChatOwnerSerializer
from .sub_objects.administrator import ChatAdministrator, ChatAdministratorSerializer
from .sub_objects.events.left import ChatMemberLeft, ChatMemberLeftSerializer
from .sub_objects.events.banned import ChatMemberBanned, ChatMemberBannedSerializer
from .sub_objects.events.restricted import ChatMemberRestricted, ChatMemberRestrictedSerializer
from .obj import ChatMember
from .serializer import ChatMemberSerializer


class ChatMemberObjectSerializer(Serializer):
    chat_member_serializers_mapping: Dict[str, Type[Serializer]] = {
        ChatMember.status.constant: ChatMemberSerializer,
        ChatOwner.status.constant: ChatOwnerSerializer,
        ChatAdministrator.status.constant: ChatAdministratorSerializer,
        ChatMemberLeft.status.constant: ChatMemberLeftSerializer,
        ChatMemberBanned.status.constant: ChatMemberBannedSerializer,
        ChatMemberRestricted.status.constant: ChatMemberRestrictedSerializer
    }

    def to_object(self, data: JsonValue) -> Any:
        status = data['status']
        serializer = self.__class__.chat_member_serializers_mapping.get(status, None)

        if serializer is None:
            raise TypeError(f"Unknown ChatMember status: '{status}'")

        return serializer().to_object(data)

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        serializer = self.__class__.chat_member_serializers_mapping.get(obj.status, None)

        if serializer is None:
            raise TypeError(f"Unknown ChatMember status: '{obj.status}'")

        return serializer().to_representation(obj, keep_none_fields=keep_none_fields)
