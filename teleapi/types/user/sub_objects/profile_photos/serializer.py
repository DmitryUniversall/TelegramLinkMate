from teleapi.core.orm.serializers.generics.serializers import ModelSerializer
from teleapi.core.orm.serializers.generics.fields import ListSerializerField,RelatedSerializerField
from .obj import UserProfilePhotos
from teleapi.types.photo_size import PhotoSizeSerializer


class UserProfilePhotosSerializer(ModelSerializer):
    photos = ListSerializerField(ListSerializerField(RelatedSerializerField(PhotoSizeSerializer())))

    class Meta:
        model = UserProfilePhotos
