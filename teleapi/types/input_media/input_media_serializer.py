from typing import Any, Dict, Type

from teleapi.core.orm.serializers import Serializer
from .sub_objects.animation import InputMediaAnimation, InputMediaAnimationSerializer
from .sub_objects.audio import InputMediaAudio, InputMediaAudioSerializer
from .sub_objects.document import InputMediaDocument, InputMediaDocumentSerializer
from .sub_objects.photo import InputMediaPhoto, InputMediaPhotoSerializer
from .sub_objects.video import InputMediaVideo, InputMediaVideoSerializer
from ...core.orm.typing import JsonValue


class InputMediaObjectSerializer(Serializer):
    input_media_serializers_mapping: Dict[str, Type[Serializer]] = {
        InputMediaAnimation.type_.constant: InputMediaAnimationSerializer,
        InputMediaAudio.type_.constant: InputMediaAudioSerializer,
        InputMediaDocument.type_.constant: InputMediaDocumentSerializer,
        InputMediaPhoto.type_.constant: InputMediaPhotoSerializer,
        InputMediaVideo.type_.constant: InputMediaVideoSerializer
    }

    def to_object(self, data: JsonValue) -> Any:
        type_ = data['type']
        serializer = self.__class__.input_media_serializers_mapping.get(type_, None)

        if serializer is None:
            raise TypeError(f"Unknown InputMedia type_: '{type_}'")

        return serializer().to_object(data)

    def to_representation(self, obj: Any, keep_none_fields: bool = True) -> JsonValue:
        serializer = self.__class__.input_media_serializers_mapping.get(obj.type_, None)

        if serializer is None:
            raise TypeError(f"Unknown InputMedia type_: '{obj.type_}'")

        return serializer().to_representation(obj, keep_none_fields=keep_none_fields)
