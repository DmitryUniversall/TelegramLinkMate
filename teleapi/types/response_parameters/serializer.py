from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ResponseParameters


class ResponseParametersSerializer(ModelSerializer):
    class Meta:
        model = ResponseParameters
