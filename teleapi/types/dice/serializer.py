from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import SelectionSerializerField, StringSerializerField
from .obj import Dice


class DiceSerializer(ModelSerializer):
    emoji = SelectionSerializerField(StringSerializerField(), ["🎲", "🎯", "🎳", "🏀", "⚽", "🎰"])

    class Meta:
        model = Dice
