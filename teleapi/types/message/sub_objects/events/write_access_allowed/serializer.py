from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import WriteAccessAllowed


class WriteAccessAllowedSerializer(ModelSerializer):
    class Meta:
        model = WriteAccessAllowed
