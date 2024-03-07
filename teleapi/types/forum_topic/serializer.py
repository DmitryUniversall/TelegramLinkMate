from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import EnumSerializerField, IntegerSerializerField
from .obj import ForumTopic
from .icon_color import ForumTopicIconRGBColor


class ForumTopicSerializer(ModelSerializer):
    icon_color = EnumSerializerField(ForumTopicIconRGBColor, IntegerSerializerField())

    class Meta:
        model = ForumTopic
