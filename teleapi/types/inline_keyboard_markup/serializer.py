from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import InlineKeyboardMarkup
from teleapi.core.orm.serializers.generics.fields import (
    ListSerializerField,
    RelatedSerializerField,
)
from .sub_objects.inline_keyboard_button import InlineKeyboardButtonSerializer


class InlineKeyboardMarkupSerializer(ModelSerializer):
    inline_keyboard = ListSerializerField(ListSerializerField(RelatedSerializerField(InlineKeyboardButtonSerializer())))

    class Meta:
        model = InlineKeyboardMarkup
