from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import PollOption


class PollOptionSerializer(ModelSerializer):
    class Meta:
        model = PollOption
