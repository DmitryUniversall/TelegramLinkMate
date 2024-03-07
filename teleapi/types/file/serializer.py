from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import File


class FileSerializer(ModelSerializer):
    class Meta:
        model = File
