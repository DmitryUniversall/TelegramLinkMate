from .model import UserModel
from .sub_objects.profile_photos import UserProfilePhotos, UserProfilePhotosSerializer
from ...core.http.request import method_request, APIMethod
from teleapi.core.utils.collections import clear_none_values


class User(UserModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, User) and other.id == self.id

    async def get_profile_photos(self, offset: int = None, limit: int = 100) -> UserProfilePhotos:
        response, data = await method_request("GET", APIMethod.GET_USER_PROFILE_PHOTOS, data=clear_none_values({
            'user_id': self.id,
            'offset': offset,
            'limit': limit
        }))

        return UserProfilePhotosSerializer().serialize(data=data['result'])
