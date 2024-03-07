from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import SwitchInlineQueryChosenChat


class SwitchInlineQueryChosenChatSerializer(ModelSerializer):
    class Meta:
        model = SwitchInlineQueryChosenChat
