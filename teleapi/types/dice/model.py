from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField, SelectionModelField


class DiceModel(Model):
    emoji: str = SelectionModelField(["🎲", "🎯", "🎳", "🏀", "⚽", "🎰"], default="🎲")
    value: int = IntegerModelField()
