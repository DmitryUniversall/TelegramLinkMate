from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import ProximityAlertTriggered
from teleapi.types.user import UserSerializer


class ProximityAlertTriggeredSerializer(ModelSerializer):
    watcher = RelatedSerializerField(UserSerializer())
    traveler = RelatedSerializerField(UserSerializer())

    class Meta:
        model = ProximityAlertTriggered
