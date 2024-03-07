from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .sub_objects.request_user import KeyboardButtonRequestUserSerializer
from .sub_objects.request_chat import KeyboardButtonRequestChatSerializer
from .sub_objects.poll_type import KeyboardButtonPollTypeSerializer
from teleapi.types.web_app_info import WebAppInfoSerializer
from .obj import KeyboardButton


class KeyboardButtonSerializer(ModelSerializer):
    request_user = RelatedSerializerField(KeyboardButtonRequestUserSerializer())
    request_chat = RelatedSerializerField(KeyboardButtonRequestChatSerializer())
    request_poll = RelatedSerializerField(KeyboardButtonPollTypeSerializer())
    web_app = RelatedSerializerField(WebAppInfoSerializer())

    class Meta:
        model = KeyboardButton
