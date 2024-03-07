from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import RelatedSerializerField
from teleapi.types.location import LocationSerializer
from .obj import ChatLocation


class ChatLocationSerializer(ModelSerializer):
    location = RelatedSerializerField(LocationSerializer())

    class Meta:
        model = ChatLocation
