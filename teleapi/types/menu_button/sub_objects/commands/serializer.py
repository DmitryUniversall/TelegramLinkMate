from ...serializer import MenuButtonSerializer
from .obj import MenuButtonCommands


class MenuButtonCommandsSerializer(MenuButtonSerializer):
    class Meta:
        model = MenuButtonCommands
