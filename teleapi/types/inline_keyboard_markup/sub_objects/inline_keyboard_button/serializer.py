from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import InlineKeyboardButton
from teleapi.types.web_app_info import WebAppInfoSerializer
from teleapi.types.login_url import LoginUrlSerializer
from teleapi.types.switch_inline_query_chosen_chat import SwitchInlineQueryChosenChatSerializer
from teleapi.types.callback_game import CallbackGameSerializer


class InlineKeyboardButtonSerializer(ModelSerializer):
    web_app = RelatedSerializerField(WebAppInfoSerializer(), is_required=False)
    login_url = RelatedSerializerField(LoginUrlSerializer(), is_required=False)
    switch_inline_query_chosen_chat = RelatedSerializerField(SwitchInlineQueryChosenChatSerializer(), is_required=False)
    callback_game = RelatedSerializerField(CallbackGameSerializer(), is_required=False)

    class Meta:
        model = InlineKeyboardButton
