from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import StringSerializerField
from .obj import MenuButton


class MenuButtonSerializer(ModelSerializer):
    type_ = StringSerializerField(read_name='type')

    class Meta:
        model = MenuButton
