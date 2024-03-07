from teleapi.core.orm.serializers.generics.fields import (
    ListSerializerField,
    RelatedSerializerField,
)
from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ReplyKeyboardMarkup
from .sub_objects.keyboard_button import KeyboardButtonSerializer


class ReplyKeyboardMarkupSerializer(ModelSerializer):
    keyboard = ListSerializerField(ListSerializerField(RelatedSerializerField(KeyboardButtonSerializer())))

    class Meta:
        model = ReplyKeyboardMarkup
