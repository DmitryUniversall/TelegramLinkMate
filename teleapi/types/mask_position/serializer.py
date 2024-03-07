from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import EnumSerializerField, StringSerializerField
from .obj import MaskPosition
from .sub_objects.mask_position_point import MaskPositionPoint


class MaskPositionSerializer(ModelSerializer):
    point = EnumSerializerField(MaskPositionPoint, StringSerializerField())

    class Meta:
        model = MaskPosition
