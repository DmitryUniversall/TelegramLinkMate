import os
from typing import List, Union

from .model import StickerModel
from teleapi.types.filelike import Filelike
from teleapi.types.file import File, FileSerializer
from teleapi.types.user import User
from ..mask_position import MaskPosition
from teleapi.core.http.request import method_request, APIMethod
from .sub_objects.sticker_format import StickerFormat
from teleapi.core.exceptions.generics import InvalidParameterError
from teleapi.core.utils.files import get_file
from teleapi.generics.http.methods.utils import make_form_data
from teleapi.types.mask_position import MaskPositionSerializer


class Sticker(StickerModel, Filelike):
    @staticmethod
    async def get_custom_emoji_stickers(custom_emoji_ids: List[str]) -> List['Sticker']:
        """
        Fetches information about custom emoji stickers by their identifiers

        :param custom_emoji_ids: `List[str]`
            List of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.

        :return: `List['Sticker']`
            Returns an Array of Sticker objects on success

        :raises:
            :raise InvalidParameterError: If Length of custom_emoji_ids is more than 200
        """

        if len(custom_emoji_ids) > 200:
            raise InvalidParameterError("Length of custom_emoji_ids must be <= 200")

        from .serializer import StickerSerializer

        response, data = await method_request("GET", APIMethod.GET_CUSTOM_EMOJI_STICKERS, data={'custom_emoji_ids': custom_emoji_ids})
        return StickerSerializer().serialize(data=data['result'])

    @staticmethod
    async def upload_sticker_file(user: Union[User, int], sticker: Union[str, bytes], sticker_format: StickerFormat) -> File:
        """
        Uploads a file with a sticker for later use in the createNewStickerSet and addStickerToSet methods (the file can be used multiple times)

        :param user: `Union[User, int]`
            User identifier or object of sticker file owner

        :param sticker: `Union[str, bytes]`
            A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format

        :param sticker_format: `StickerFormat`
            Format of the sticker

        :return: `File`
            Returns the uploaded File on success.
        """

        if isinstance(sticker, str) and os.path.exists(sticker):
            _, sticker = get_file(sticker)

        form_data = make_form_data({
            'user_id': user.id if isinstance(user, User) else user,
            'sticker_format': sticker_format.value
        })

        form_data.add_field('sticker', sticker)

        response, data = await method_request(
            "POST",
            APIMethod.UPLOAD_STICKER_FILE,
            data=form_data
        )

        return FileSerializer().serialize(data=data['result'])

    @staticmethod
    async def set_emoji_list(sticker_file_id: str, emoji_list: List[str]) -> bool:
        """
        Changes the list of emoji assigned to a regular or custom emoji sticker.
        The sticker must belong to a sticker set created by the bot.

        :param sticker_file_id: `str`
            File identifier of the sticker

        :param emoji_list: `List[str]`
            1-20 emoji associated with the sticker

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: If length of emoji_list is greater than 20 or equals 0
        """

        if not (1 <= len(emoji_list) <= 20):
            raise InvalidParameterError("Length of custom_emoji_ids must be from 1 to 20")

        response, data = await method_request("POST", APIMethod.SET_STICKER_EMOJI_LIST, data={
            "sticker": sticker_file_id,
            "emoji_list": emoji_list
        })

        return bool(data["result"])

    @staticmethod
    async def set_keywords(sticker_file_id: str, keywords: List[str]) -> bool:
        """
        Changes search keywords assigned to a regular or custom emoji sticker.
        The sticker must belong to a sticker set created by the bot.

        :param sticker_file_id: `str`
            File identifier of the sticker

        :param keywords: `List[str]`
            List of 0-20 search keywords for the sticker with total length of up to 64 characters

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: If length of emoji_list is greater than 20 or equals 0
        """

        if not (1 <= len(keywords) <= 20):
            raise InvalidParameterError("Length of keywords must be from 1 to 20")
        elif any([len(keyword) > 64 for keyword in keywords]):
            raise InvalidParameterError("Each keyword of keywords list must be from 1 to 64 characters long")

        response, data = await method_request("POST", APIMethod.SET_STICKER_KEYWORDS, data={
            "sticker": sticker_file_id,
            "keywords": keywords
        })

        return bool(data["result"])

    @staticmethod
    async def set_mask_position(sticker_file_id: str, mask_position: MaskPosition) -> bool:
        """
        Changes the mask position of a mask sticker.
        The sticker must belong to a sticker set that was created by the bot.

        :param sticker_file_id: `str`
            File identifier of the sticker

        :param mask_position: `MaskPosition`
            Object with the position where the mask should be placed on faces.
            Omit the parameter to remove the mask position.

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("POST", APIMethod.SET_STICKER_MASK_POSITION, data={
            "sticker": sticker_file_id,
            "mask_position": MaskPositionSerializer().serialize(obj=mask_position)
        })

        return bool(data["result"])
