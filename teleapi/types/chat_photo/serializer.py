from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ChatPhoto


class ChatPhotoSerializer(ModelSerializer):
    class Meta:
        model = ChatPhoto
