from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.user import UserSerializer
from teleapi.types.chat import ChatSerializer
from teleapi.types.chat_member import ChatMemberObjectSerializer
from .obj import ChatMemberUpdated


class ChatMemberUpdatedSerializer(ModelSerializer):
    chat = RelatedSerializerField(ChatSerializer())
    user = RelatedSerializerField(UserSerializer(), read_name="from")
    old_chat_member = RelatedSerializerField(ChatMemberObjectSerializer())
    new_chat_member = RelatedSerializerField(ChatMemberObjectSerializer())

    class Meta:
        model = ChatMemberUpdated
