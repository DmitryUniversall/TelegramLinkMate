from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import StringSerializerField
from .obj import TelegramBotCommandScope


class TelegramBotCommandScopeSerializer(ModelSerializer):
    type_ = StringSerializerField(read_name='type')

    class Meta:
        model = TelegramBotCommandScope
