from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ReplyKeyboardRemove


class ReplyKeyboardRemoveSerializer(ModelSerializer):
    class Meta:
        model = ReplyKeyboardRemove
