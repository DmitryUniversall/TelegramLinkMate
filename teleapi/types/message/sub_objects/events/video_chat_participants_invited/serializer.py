from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import ListSerializerField, RelatedSerializerField
from .obj import VideoChatParticipantsInvited
from teleapi.types.user import UserSerializer


class VideoChatParticipantsInvitedSerializer(ModelSerializer):
    users = ListSerializerField(RelatedSerializerField(UserSerializer()))

    class Meta:
        model = VideoChatParticipantsInvited
