from typing import TYPE_CHECKING, List
from typing import Union

from aiohttp import FormData

from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.http.request.api_request import method_request
from teleapi.core.utils.collections import clear_none_values, exclude_from_dict
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.forece_reply import ForceReply
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
from teleapi.types.input_media.input_media_serializer import InputMediaObjectSerializer
from teleapi.types.input_media.sub_objects.audio import InputMediaAudio
from teleapi.types.input_media.sub_objects.document import InputMediaDocument
from teleapi.types.input_media.sub_objects.photo import InputMediaPhoto
from teleapi.types.input_media.sub_objects.video import InputMediaVideo
from teleapi.types.location import LocationSerializer, Location
from teleapi.types.message_entity import MessageEntity, MessageEntitySerializer
from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup
from .utils import get_converted_reply_markup
from ..utils import make_form_data

if TYPE_CHECKING:
    from teleapi.types.message import Message
    from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from teleapi.core.ui.inline_view.view import BaseInlineView
    from teleapi.types.poll import Poll


async def edit_message(method: APIMethod,
                       chat_id: Union[int, str] = None,
                       message_id: int = None,
                       inline_message_id: str = None,
                       reply_markup: Union[
                           'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                       view: 'BaseInlineView' = None,
                       **kwargs
                       ) -> Union['Message', bool]:
    """
    Sends the message of any type (text, photo, video...)

    :param method: `ApiMethod`
        Api method to send the message

    :param chat_id: `Union[int, str]`
        Required if inline_message_id is not specified.
        Unique identifier for the target chat or username of the target channel (in the format @channelusername)

    :param message_id: `int`
        Required if inline_message_id is not specified. Identifier of the message to edit

    :param inline_message_id: `str`
        Required if chat_id and message_id are not specified. Identifier of the inline message

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control message interface.

    :param kwargs: `dict`
        (Optional) Any other request parameters

    :return: `Union['Message', List['Message']]`
        The sent message.

    :raises:
        :raise ApiRequestError: ApiRequestError or any of its subclasses if request sent to the Telegram Bot API failed
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        :raise ValueError: If (chat_id and message_id) or inline_message_id was not specified
    """

    if not all((chat_id, message_id)) and not inline_message_id:
        raise ValueError("You must specify (message_id and chat_id) or inline_message_id")

    reply_markup = await get_converted_reply_markup(reply_markup, view)

    form_data = None

    try:
        form_data = kwargs.pop('form_data')
    except KeyError:
        pass

    request_data = make_form_data(clear_none_values(
        {
            **exclude_from_dict(locals(), 'view', 'kwargs', 'method', 'form_data'),
            **kwargs
        }
    ), form_data=form_data)

    response, data = await method_request("POST", method, data=request_data)

    if data['result'] == 'true':
        return True

    from teleapi.types.message.serializer import MessageSerializer
    message = MessageSerializer().serialize(data=data['result'], many=isinstance(data['result'], list))

    if view:
        if isinstance(message, list):
            view.message = message[-1]
        else:
            view.message = message

    return message


async def edit_message_text(text: str,
                            parse_mode: ParseMode = ParseMode.NONE,
                            disable_web_page_preview: bool = None,
                            entities: List['MessageEntity'] = None,
                            **kwargs
                            ) -> Union['Message', bool]:
    """
    Edits text and game messages.

    :param text: `str`
        The text of the message to be edited.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the message text.
        Default is `ParseMode.NONE`.

    :param disable_web_page_preview: `bool`
        (Optional) Disable web page previews for links in the message.

    :param entities: `List['MessageEntity']`
        (Optional) List of special entities that appear in the message text.

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    """

    parse_mode = parse_mode.value
    entities = MessageEntitySerializer().serialize(
        obj=entities,
        many=True,
        keep_none_fields=False
    ) if entities is not None else None

    return await edit_message(
        method=APIMethod.EDIT_MESSAGE_TEXT,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def edit_message_caption(caption: str,
                               parse_mode: ParseMode = ParseMode.NONE,
                               caption_entities: List['MessageEntity'] = None,
                               **kwargs
                               ) -> Union['Message', bool]:
    """
    Edits captions of messages

    :param caption: `str`
        The caption of the message to be edited.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the message text.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities that appear in the message caption.

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    """

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None

    return await edit_message(
        method=APIMethod.EDIT_MESSAGE_CAPTION,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def edit_message_media(media: Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo],
                             **kwargs
                             ) -> Union['Message', bool]:
    """
    Edits animation, audio, document, photo, or video messages

    :param media: `Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]`
        Media object to be edited

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.

    :raises:
        :raise ValueError: If media object has 'data' or 'thumbnail_data', but has no 'filename' or 'thumbnail_filename'

    Notes:
     - If a message is part of a message album, then it can be edited only to an audio for audio albums,
       only to a document for document albums and to a photo or a video otherwise.
     - When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL.
    """

    form_data = FormData()

    if media.data is not None:
        if media.filename is None:
            raise ValueError(f"filename was not specified")

        form_data.add_field(media.filename, media.data)

    if hasattr(media, 'thumbnail_data') and media.thumbnail_data is not None:
        if media.thumbnail_filename is None:
            raise ValueError(f"thumbnail_filename was not specified")

        form_data.add_field(media.thumbnail_filename, media.thumbnail_data)

    media = InputMediaObjectSerializer().serialize(obj=media, keep_none_fields=False)

    return await edit_message(
        method=APIMethod.EDIT_MESSAGE_MEDIA,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def edit_message_reply_markup(reply_markup: Union[
    'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                    view: 'BaseInlineView' = None,
                                    **kwargs
                                    ) -> Union['Message', bool]:
    """
    Edits message reply_markup

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `'BaseInlineView'`
        (Optional) Inline view to control message interface.

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    """

    return await edit_message(
        method=APIMethod.EDIT_MESSAGE_REPLY_MARKUP,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def edit_message_live_location(location: Location, **kwargs) -> Union['Message', bool]:
    """
    Edits live location messages.
    A location can be edited until its live_period expires or editing is explicitly disabled by a call to stopMessageLiveLocation.

    :param location: `Location`
        ParameterDescription

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    """

    location_data = LocationSerializer().serialize(obj=location)

    return await edit_message(
        method=APIMethod.EDIT_MESSAGE_LIVE_LOCATION,
        **exclude_from_dict(location_data, 'live_period'),
        **kwargs
    )


async def stop_message_live_location(**kwargs) -> Union['Message', bool]:
    """
    Stops updating a live location message before live_period expires

    :param kwargs: `dict`
        Other parameters specified in `edit_message` function above

    :return: `Union['Message', bool]`
        On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned.
    """

    return await edit_message(
        method=APIMethod.STOP_MESSAGE_LIVE_LOCATION,
        **kwargs
    )


async def stop_poll(chat_id: Union[int, str],
                    message_id: int,
                    reply_markup: Union[
                        'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict],
                    view: 'BaseInlineView'
                    ) -> 'Poll':
    """
    Stops a poll which was sent by the bot

    :param chat_id: `Union[int, str]`
        Required if inline_message_id is not specified.
        Unique identifier for the target chat or username of the target channel (in the format @channelusername)

    :param message_id: `int`
        Required if inline_message_id is not specified. Identifier of the message to edit

    :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
        (Optional) Additional interface for the message.

    :param view: `BaseInlineView`
        (Optional) Inline view to control message interface.

    :return: `Poll`
        On success, the stopped Poll is returned.

    :raises:
        :raise ApiRequestError: ApiRequestError or any of its subclasses if request sent to the Telegram Bot API failed
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        :raise ValueError: If (chat_id and message_id) or inline_message_id was not specified
    """

    reply_markup = await get_converted_reply_markup(reply_markup, view)

    request_data = make_form_data(clear_none_values({
        **exclude_from_dict(locals(), 'view'),
        **kwargs
    }))

    from teleapi.types.poll import PollSerializer

    response, data = await method_request("POST", APIMethod.STOP_POLL, data=request_data)
    return PollSerializer().serialize(data=data)
