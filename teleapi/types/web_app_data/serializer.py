from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import WebAppData


class WebAppDataSerializer(ModelSerializer):
    class Meta:
        model = WebAppData
