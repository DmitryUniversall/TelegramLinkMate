from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import ForceReply


class ForceReplySerializer(ModelSerializer):
    class Meta:
        model = ForceReply
