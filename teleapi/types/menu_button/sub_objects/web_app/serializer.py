from ...serializer import MenuButtonSerializer
from .obj import MenuButtonWebApp
from teleapi.core.orm.serializers import RelatedSerializerField
from teleapi.types.web_app_info import WebAppInfoSerializer


class MenuButtonWebAppSerializer(MenuButtonSerializer):
    web_app = RelatedSerializerField(WebAppInfoSerializer())

    class Meta:
        model = MenuButtonWebApp
