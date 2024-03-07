from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from .obj import Venue
from teleapi.types.location import LocationSerializer


class VenueSerializer(ModelSerializer):
    location = RelatedSerializerField(LocationSerializer())

    class Meta:
        model = Venue
