from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import KeyboardButtonRequestChat
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRightsSerializer


class KeyboardButtonRequestChatSerializer(ModelSerializer):
    bot_administrator_rights = RelatedSerializerField(ChatAdministratorRightsSerializer(), is_required=False)
    user_administrator_rights = RelatedSerializerField(ChatAdministratorRightsSerializer(), is_required=False)

    class Meta:
        model = KeyboardButtonRequestChat
