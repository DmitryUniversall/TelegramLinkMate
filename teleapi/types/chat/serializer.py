from teleapi.core.orm.serializers.generics.fields import (
    StringSerializerField,
    RelatedSerializerField,
    ListSerializerField,
    EnumSerializerField
)
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Chat
from .chat_type import ChatType
from ..chat_photo import ChatPhotoSerializer
from ..location.sub_objects.chat_location import ChatLocationSerializer
from teleapi.types.chat_permissions import ChatPermissionsSerializer


class ChatSerializer(ModelSerializer):
    type_ = EnumSerializerField(ChatType, StringSerializerField(), read_name="type")
    active_usernames = ListSerializerField(StringSerializerField(), is_required=False, default=[])
    pinned_message = RelatedSerializerField('MessageSerializer', is_required=False)

    location = RelatedSerializerField(ChatLocationSerializer(), is_required=False)
    permissions = RelatedSerializerField(ChatPermissionsSerializer(), is_required=False)
    photo = RelatedSerializerField(ChatPhotoSerializer(), is_required=False)

    class Meta:
        model = Chat
