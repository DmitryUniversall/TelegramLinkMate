from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import StringSerializerField, RelatedSerializerField
from .obj import MessageEntity
from teleapi.types.user import UserSerializer


class MessageEntitySerializer(ModelSerializer):
    type_ = StringSerializerField(read_name="type")
    user = RelatedSerializerField(UserSerializer(), is_required=False)

    class Meta:
        model = MessageEntity
