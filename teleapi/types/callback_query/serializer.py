from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.user.serializer import UserSerializer
from teleapi.types.message.serializer import MessageSerializer
from .obj import CallbackQuery


class CallbackQuerySerializer(ModelSerializer):
    user = RelatedSerializerField(UserSerializer(), read_name='from')
    message = RelatedSerializerField(MessageSerializer(), is_required=False)

    class Meta:
        model = CallbackQuery
        exclude = ('is_answered',)
