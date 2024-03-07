from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import UserShared


class UserSharedSerializer(ModelSerializer):
    class Meta:
        model = UserShared
