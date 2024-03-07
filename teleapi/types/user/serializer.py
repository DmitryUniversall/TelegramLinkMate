from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
