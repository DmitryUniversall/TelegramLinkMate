import os
import string
from typing import Union, List

from teleapi.core.http.request import method_request, APIMethod
from teleapi.types.input_sticker import InputSticker, InputStickerSerializer
from teleapi.types.sticker.sub_objects.sticker_format import StickerFormat
from teleapi.types.sticker.sub_objects.sticker_type import StickerType
from teleapi.types.user import User
from .model import StickerSetModel
from teleapi.core.state import project_settings
from teleapi.core.exceptions.generics import InvalidParameterError
from ...core.utils.files import get_file
from ...generics.http.methods.utils import make_form_data


class StickerSet(StickerSetModel):
    @staticmethod
    async def get_sticker_set(name: str) -> 'StickerSet':
        """
        Fetches a sticker set

        :param name: `str`
            Name of the sticker set

        :return: `StickerSet`
            StickerSet on success
        """

        from .serializer import StickerSetSerializer

        response, data = await method_request("GET", APIMethod.GET_STICKER_SET, data={'name': name})
        return StickerSetSerializer().serialize(data=data['result'])

    @staticmethod
    async def create_sticker_set(user: Union[User, int],
                                 name: str,
                                 title: str,
                                 stickers: List[InputSticker],
                                 sticker_format: StickerFormat,
                                 sticker_type: StickerType = StickerType.REGULAR,
                                 needs_repainting: bool = None
                                 ) -> 'StickerSet':
        """
        Creates a new sticker set owned by a user. The bot will be able to edit the sticker set thus created

        :param user: `Union[User, int]`
            User object or identifier of created sticker set owner

        :param name: `str`
            Short name of sticker set, to be used in `t.me/addstickers/` URLs (e.g., animals).
            Can contain only English letters, digits and underscores.
            Must begin with a letter, can't contain consecutive underscores and must end in "_by_<bot_username>".
            <bot_username> is case-insensitive. 1-64 characters.

        :param title: `str`
            Sticker set title, 1-64 characters

        :param stickers: `List[InputSticker]`
            List of 1-50 initial stickers to be added to the sticker set

        :param sticker_format: `StickerFormat`
            Format of stickers in the set

        :param sticker_type: `StickerType`
            Type of stickers in the set. By default, a regular sticker set is created.

        :param needs_repainting: `bool`
            Pass True if stickers in the sticker set must be repainted to the color of text when used in messages,
            the accent color if used as emoji status, white on chat photos, or another appropriate color based on context;
            for custom emoji sticker sets only

        :return: `StickerSet`
            Returns created StickerSet object

        :raises:
            :raise InvalidParameterError: If format of the input parameters is incorrect (check docs above)
            :raise ValueError: If sticker filename is not specified
        """

        if not (1 <= len(name) <= 64):
            raise InvalidParameterError("Sticker set name must be <= 64 characters long")
        elif not name.endswith(f"_by_{project_settings.BOT.me.username}"):
            raise InvalidParameterError('Sticker set name must ends with "_by_<bot_username>"')
        elif not all([char in (string.ascii_letters + string.digits + "_") for char in name]):
            raise InvalidParameterError("Sticker set name can contain only English letters, digits and underscores")
        elif any([name[index] == "_" and name[index + 1] == "_" for index in range(len(name) - 1)]):
            raise InvalidParameterError("Sticker set name can't contain consecutive underscores")
        elif not (1 <= len(title) <= 64):
            raise InvalidParameterError("Sticker set title must be <= 64 characters long")
        elif not (1 <= len(stickers) <= 50):
            raise InvalidParameterError("Length of initial stickers list must be from 1 to 50")

        form_data = make_form_data({
            "user": user.id if isinstance(user, User) else user,
            "name": name,
            "title": title,
            "sticker_format": sticker_format.value,
            "sticker_type": sticker_type.value,
            "needs_repainting": needs_repainting
        })

        serialized_stickers = []

        for sticker in stickers:
            if sticker.data is not None:
                if sticker.filename is None:
                    raise ValueError(f"filename is not specified")

                form_data.add_field(sticker.filename, sticker.data)

            serialized_stickers.append(
                InputStickerSerializer().serialize(obj=sticker, keep_none_fields=False)
            )

        form_data.add_field("stickers", serialized_stickers)

        _, __ = await method_request("POST", APIMethod.CREATE_STICKER_SET, data=form_data)
        return await StickerSet.get_sticker_set(name)

    async def add_sticker(self, user: Union[User, int], sticker: InputSticker, self_update: bool = False) -> bool:
        """
        Adds a new sticker to a set created by the bot.
        The format of the added sticker must match the format of the other stickers in the set.
        Emoji sticker sets can have up to 200 stickers. Animated and video sticker sets can have up to 50 stickers.
        Static sticker sets can have up to 120 stickers

        :param user: `Union[User, int]`
            User identifier or object of sticker set owner

        :param sticker: `InputSticker`
            Sticker to be added. If exactly the same sticker had already been added to the set, then the set isn't changed.

        :param self_update: `bool`
            If True, new StickerSet (StickerSet.stickers) data will be fetched for this object

        :return: `bool`
            Returns True on success
        """

        if (self.is_video or self.is_animated) and len(self.stickers) >= 50:
            raise OverflowError("Animated and video sticker sets can have up to 50 stickers")
        elif len(self.stickers) >= 200:
            raise OverflowError("Sticker sets can have up to 200 stickers")

        form_data = make_form_data({
            "user": user.id if isinstance(user, User) else user,
            "name": self.name
        })

        if sticker.data is not None:
            if sticker.filename is None:
                raise ValueError(f"filename is not specified")

            form_data.add_field(sticker.filename, sticker.data)

        form_data.add_field("sticker", InputStickerSerializer().serialize(obj=sticker, keep_none_fields=False))

        response, data = await method_request("POST", APIMethod.ADD_STICKER_TO_SET, data=form_data)

        if self_update:
            sticker_set = await StickerSet.get_sticker_set(self.name)
            self.stickers = sticker_set.stickers

        return bool(data["result"])

    async def set_sticker_position(self, sticker_file_id: str, position: int, self_update: bool = False) -> bool:  # TODO: Make classmethod?
        """
        Moves a sticker in a set created by the bot to a specific position.

        :param sticker_file_id: `str`
            File identifier of the sticker

        :param position: `int`
            New sticker position in the set, zero-based

        :param self_update: `bool`
            If True, new StickerSet (StickerSet.stickers) data will be fetched for this object

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("POST", APIMethod.SET_STICKER_POSITION_IN_SET, data={
            "sticker": sticker_file_id,
            "position": position
        })

        if self_update:
            sticker_set = await StickerSet.get_sticker_set(self.name)
            self.stickers = sticker_set.stickers

        return bool(data["result"])

    async def delete_sticker(self, sticker_file_id: str, self_update: bool = False) -> bool:  # TODO: Make classmethod?
        """
        Deletes a sticker from a set created by the bot.

        :param sticker_file_id: `str`
            File identifier of the sticker

        :param self_update: `bool`
            If True, new StickerSet (StickerSet.stickers) data will be fetched for this object

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("POST", APIMethod.DELETE_STICKER_FROM_SET, data={
            "sticker": sticker_file_id,
        })

        if self_update:
            sticker_set = await StickerSet.get_sticker_set(self.name)
            self.stickers = sticker_set.stickers

        return bool(data["result"])

    async def set_title(self, title: str) -> bool:
        """
        Sets the title of sticker set

        :param title: `str`
            Sticker set title, 1-64 characters

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: If length of title is greater than 64 or equals 0
        """

        if not (1 <= len(title) <= 64):
            raise InvalidParameterError("Length of keywords must be from 1 to 64")

        response, data = await method_request("POST", APIMethod.SET_STICKER_SET_TITLE, data={
            "name": self.name,
            "title": title
        })

        return bool(data["result"])

    async def set_thumbnail(self, user: Union[User, int], thumbnail: Union[bytes, str]) -> bool:
        """
        Sets the thumbnail of a regular or mask sticker set.
        The format of the thumbnail file must match the format of the stickers in the set.

        :param user: `Union[User, int]`
            User identifier or object of the sticker set owner

        :param thumbnail: `Union[bytes, str]`
            A .WEBP or .PNG image with the thumbnail,
            must be up to 128 kilobytes in size and have a width and height of exactly 100px,
            or a .TGS animation with a thumbnail up to 32 kilobytes in size,
            or a WEBM video with the thumbnail up to 32 kilobytes in size;
            Pass a file_id as a String to send a file that already exists on the Telegram servers,
            pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data.
            Animated and video sticker set thumbnails can't be uploaded via HTTP URL.
            If omitted, then the thumbnail is dropped and the first sticker is used as the thumbnail.

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: if sticker set type is not `StickerType.REGULAR` or `StickerType.MASK`
        """

        if self.sticker_type not in (StickerType.REGULAR, StickerType.MASK):
            raise InvalidParameterError("Sticker set type must be StickerType.REGULAR or StickerType.MASK")

        form_data = make_form_data({
            "user": user.id if isinstance(user, User) else user,
        })

        if isinstance(thumbnail, str) and os.path.exists(thumbnail):
            _, thumbnail = get_file(thumbnail)
        form_data.add_field("thumbnail", thumbnail)

        response, data = await method_request("POST", APIMethod.SET_STICKER_SET_THUMBNAIL, data=form_data)

        return bool(data["result"])

    async def delete(self) -> bool:
        """
        Deletes a sticker set that was created by the bot

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("POST", APIMethod.SET_STICKER_SET_THUMBNAIL, data={
            "name": self.name
        })

        return bool(data["result"])
