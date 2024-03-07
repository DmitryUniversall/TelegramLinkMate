from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import ChatInviteLink
from teleapi.types.user import UserSerializer


class ChatInviteLinkSerializer(ModelSerializer):
    creator = RelatedSerializerField(UserSerializer())

    class Meta:
        model = ChatInviteLink
