from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import TelegramBotCommand


class TelegramBotCommandSerializer(ModelSerializer):
    class Meta:
        model = TelegramBotCommand
