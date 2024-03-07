from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Location


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
