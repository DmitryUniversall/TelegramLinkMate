from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import VoidSerializerField
from .obj import InputFile


class InputMediaSerializer(ModelSerializer):
    data = VoidSerializerField()
    filename = VoidSerializerField()

    class Meta:
        model = InputFile
