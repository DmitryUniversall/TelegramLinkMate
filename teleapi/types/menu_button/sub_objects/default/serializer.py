from ...serializer import MenuButtonSerializer
from .obj import MenuButtonDefault


class MenuButtonDefaultSerializer(MenuButtonSerializer):
    class Meta:
        model = MenuButtonDefault
