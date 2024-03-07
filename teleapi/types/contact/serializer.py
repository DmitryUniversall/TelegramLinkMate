from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from .obj import Contact


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact

