from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField, StringSerializerField
from .obj import ChatMember
from teleapi.types.user import UserSerializer


class ChatMemberSerializer(ModelSerializer):
    user = RelatedSerializerField(UserSerializer())
    status = StringSerializerField()

    class Meta:
        model = ChatMember
