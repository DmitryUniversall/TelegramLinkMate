from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Filelike


class FilelikeSerializer(ModelSerializer):
    class Meta:
        model = Filelike
