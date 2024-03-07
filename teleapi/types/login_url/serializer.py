from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import LoginUrl


class LoginUrlSerializer(ModelSerializer):
    class Meta:
        model = LoginUrl
