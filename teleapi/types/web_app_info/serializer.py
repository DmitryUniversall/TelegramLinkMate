from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import WebAppInfo


class WebAppInfoSerializer(ModelSerializer):
    class Meta:
        model = WebAppInfo
