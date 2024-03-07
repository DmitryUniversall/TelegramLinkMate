import os
from datetime import datetime
from typing import TYPE_CHECKING, List
from typing import Union

from aiohttp import FormData

from teleapi.core.exceptions.generics import FileTooLargeError, InvalidParameterError
from teleapi.core.http.request.api_method import APIMethod
from teleapi.core.http.request.api_request import method_request
from teleapi.core.utils.collections import clear_none_values, exclude_from_dict
from teleapi.core.utils.files import get_file
from teleapi.core.utils.syntax import default
from teleapi.enums.parse_mode import ParseMode
from teleapi.generics.http.methods.utils import make_form_data
from teleapi.types.contact import Contact, ContactSerializer
from teleapi.types.input_media.input_media_serializer import InputMediaObjectSerializer
from teleapi.types.input_media.sub_objects.audio import InputMediaAudio
from teleapi.types.input_media.sub_objects.document import InputMediaDocument
from teleapi.types.input_media.sub_objects.photo import InputMediaPhoto
from teleapi.types.input_media.sub_objects.video import InputMediaVideo
from teleapi.types.location import Location, LocationSerializer
from teleapi.types.message_entity import MessageEntity, MessageEntitySerializer
from .utils import get_converted_reply_markup

if TYPE_CHECKING:
    from teleapi.types.message import Message
    from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from teleapi.core.ui.inline_view.view import BaseInlineView
    from teleapi.types.forece_reply import ForceReply
    from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
    from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup
    from teleapi.types.poll.sub_object import PollType


async def send(method: APIMethod,  # TODO: Thumbnail attach with filename attach://<file_attach_name>
               chat_id: int,
               message_thread_id: int = None,
               disable_notification: bool = None,
               protect_content: bool = None,
               reply_to_message_id: int = None,
               allow_sending_without_reply: bool = None,
               reply_markup: Union[
                   'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
               view: 'BaseInlineView' = None,
               **kwargs
               ) -> Union['Message', List['Message']]:
    """
    Sends the message of any type (text, photo, video...)

    :param method: `ApiMethod`
        Api method to send the message

    :param chat_id: `Union[int, str]`
        The unique identifier or username of the target chat.

    :param reply_to_message_id: `int`
        (Optional) If the message is a reply, the ID of the original message.

    :param message_thread_id: `int`
        (Optional) Unique identifier of a message thread to which the message belongs; for supergroups only

    :param disable_notification: `bool`
        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param protect_content: `bool`
        (Optional) Mark the message as protected content.

    :param allow_sending_without_reply: `bool`
        (Optional) Pass True if the message should be sent even if the specified replied-to message is not found

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
    """

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

    from teleapi.types.message.serializer import MessageSerializer
    response, data = await method_request("POST", method, data=request_data)
    message = MessageSerializer().serialize(data=data['result'], many=isinstance(data['result'], list))

    if view:
        if isinstance(message, list):
            view.message = message[-1]
        else:
            view.message = message

    return message


async def send_message(text: str,
                       parse_mode: ParseMode = ParseMode.NONE,
                       disable_web_page_preview: bool = None,
                       entities: List['MessageEntity'] = None,
                       **kwargs
                       ) -> 'Message':
    """
    Sends a text message to a specified chat

    :param text: `str`
        The text of the message to be sent.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the message text.
        Default is `ParseMode.NONE`.

    :param disable_web_page_preview: `bool`
        (Optional) Disable web page previews for links in the message.

    :param entities: `List['MessageEntity']`
        (Optional) List of special entities that appear in the message text.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message.
    """

    parse_mode = parse_mode.value
    entities = MessageEntitySerializer().serialize(
        obj=entities,
        many=True,
        keep_none_fields=False
    ) if entities is not None else None

    return await send(
        method=APIMethod.SEND_MESSAGE,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def send_photo(photo: Union[bytes, str],
                     caption: str = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     has_spoiler: bool = None,
                     filename: str = None,
                     **kwargs
                     ) -> 'Message':
    """
    Sends a photo to a specified chat

    :param photo: `Union[bytes, str]`
        The photo file to be sent. It can be provided as bytes, a file path (str), or the file_id of a photo file that
        already exists on the Telegram servers (str).

    :param caption: `str`
        (Optional) A caption to accompany the photo.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param has_spoiler: `bool`
        (Optional) Mark the photo as containing spoilers.

    :param filename: `str`
        (Optional) The filename to be used when sending the photo.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message.

    :raises:
        :raise FileTooLargeError: If specified photo is more than 10MB in size
    """

    if isinstance(photo, str) and not photo.startswith("https://"):
        filename, photo = get_file(photo)

        if (len(photo) // 1024) // 1024 > 10:
            raise FileTooLargeError(
                f"Specified photo must be less than 10MB in size, got {(len(photo) // 1024) // 1024}kB"
            )

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None
    form_data = FormData()
    form_data.add_field('photo', photo, filename=filename)

    return await send(
        method=APIMethod.SEND_PHOTO,
        **exclude_from_dict(locals(), 'filename', 'kwargs', 'photo'),
        **kwargs
    )


async def send_audio(audio: Union[bytes, str],
                     caption: str = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     duration: int = None,
                     performer: str = None,
                     title: str = None,
                     thumbnail: Union[bytes, str] = None,
                     filename: str = None,
                     **kwargs
                     ) -> 'Message':
    """
    Sends an audio file to a specified chat

    :param audio: `Union[bytes, str]`
        The audio file to be sent. It can be provided as bytes, a file path (str), or the file_id of an audio file that
        already exists on the Telegram servers.

    :param caption: `str`
        (Optional) A caption to accompany the audio.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param duration: `int`
        (Optional) Duration of the audio in seconds.

    :param performer: `str`
        (Optional) Performer of the audio.

    :param title: `str`
        (Optional) Title of the audio.

    :param thumbnail: `Union[bytes, str]`
        (Optional) Thumbnail of the audio, can be provided as bytes or a file path.

    :param filename: `str`
        (Optional) The filename to be used when sending the audio.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message.

    :raises:
        :raise FileTooLargeError: If specified thumbnail is more than 200kB in size

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size.
          A thumbnail's width and height should not exceed 320.
    """

    if isinstance(audio, str) and os.path.exists(audio):
        filename, audio = get_file(audio)
    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

        if len(thumbnail) // 1024 > 200:
            raise FileTooLargeError(
                f"Specified thumbnail must be less than 200kB in size, got {len(thumbnail) // 1024}kB")

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None
    form_data = FormData()

    if thumbnail:
        form_data.add_field('thumbnail', thumbnail)
    form_data.add_field('audio', audio, filename=filename)

    return await send(
        method=APIMethod.SEND_AUDIO,
        **exclude_from_dict(locals(), 'filename', 'kwargs', 'audio', 'thumbnail'),
        **kwargs
    )


async def send_document(document: Union[bytes, str],
                        caption: str = None,
                        parse_mode: ParseMode = ParseMode.NONE,
                        caption_entities: List['MessageEntity'] = None,
                        disable_content_type_detection: bool = None,
                        thumbnail: Union[bytes, str] = None,
                        filename: str = None,
                        **kwargs
                        ) -> 'Message':
    """
    Sends a document file to a specified chat.

    :param document: `Union[bytes, str]`
        The document file to be sent. It can be provided as bytes, a file path (str), or the file_id of a document file
        that already exists on the Telegram servers.

    :param caption: `str`
        (Optional) A caption to accompany the document.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param disable_content_type_detection: `bool`
        (Optional) Disables automatic content type detection for the document.

    :param thumbnail: `Union[bytes, str]`
        (Optional) Thumbnail of the document, can be provided as bytes or a file path.

    :param filename: `str`
        (Optional) The filename to be used when sending the document.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.

    :raises:
        :raise FileTooLargeError: If specified document is mode than 50MB in size
        or thumbnail is more than 200kB in size

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size.
          A thumbnail's width and height should not exceed 320.
    """

    if isinstance(document, str) and os.path.exists(document):
        filename, document = get_file(document)

        if (len(document) // 1024) // 1024 > 50:
            raise FileTooLargeError(
                f"Specified document must be less than 50MB in size, got {(len(document) // 1024) // 1024}kB")

    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

        if len(thumbnail) // 1024 > 200:
            raise FileTooLargeError(
                f"Specified thumbnail must be less than 200kB in size, got {len(thumbnail) // 1024}kB")

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None
    form_data = FormData()

    if thumbnail:
        form_data.add_field('thumbnail', thumbnail)
    form_data.add_field('document', document, filename=filename)

    return await send(
        method=APIMethod.SEND_DOCUMENT,
        **exclude_from_dict(locals(), 'filename', 'kwargs', 'document', "thumbnail"),
        **kwargs
    )


async def send_video(video: Union[bytes, str],
                     thumbnail: Union[bytes, str] = None,
                     caption: str = None,
                     duration: int = None,
                     height: int = None,
                     width: int = None,
                     has_spoiler: bool = None,
                     supports_streaming: bool = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     filename: str = None,
                     **kwargs
                     ) -> 'Message':
    """
    Sends a video to a specified chat.

    :param video: `Union[bytes, str]`
        The video to be sent. It can be provided as bytes, a file path (str), or the file_id of a video file
        that already exists on the Telegram servers.

    :param thumbnail: `Union[bytes, str]`
        The thumbnail of the video. It should be provided as bytes or a file path.

    :param caption: `str`
        (Optional) A caption to accompany the video.

    :param duration: `int`
        (Optional) Duration of the video in seconds.

    :param height: `int`
        (Optional) Height of the video in pixels.

    :param width: `int`
        (Optional) Width of the video in pixels.

    :param has_spoiler: `bool`
        (Optional) Mark the video as containing spoilers.

    :param supports_streaming: `bool`
        (Optional) If True, the video supports streaming.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

        (Optional) Sends the message silently. Users will receive a notification with no sound.

    :param filename: `str`
        (Optional) The filename to be used when sending the video.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.

    :raises:
        :raise FileTooLargeError: If specified thumbnail is more than 200kB in size

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size.
          A thumbnail's width and height should not exceed 320.
    """

    if isinstance(video, str) and os.path.exists(video):
        filename, video = get_file(video)
    if isinstance(thumbnail, str) and os.path.exists(video):
        _, thumbnail = get_file(thumbnail)

        if len(thumbnail) // 1024 > 200:
            raise FileTooLargeError(
                f"Specified thumbnail must be less than 200kB in size, got {len(thumbnail) // 1024}kB")

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None
    form_data = FormData()

    if thumbnail:
        form_data.add_field('thumbnail', thumbnail)
    form_data.add_field('video', video, filename=filename)

    return await send(
        method=APIMethod.SEND_VIDEO,
        **exclude_from_dict(locals(), 'filename', 'kwargs', 'video', "thumbnail"),
        **kwargs
    )


async def send_animation(animation: Union[bytes, str],
                         thumbnail: Union[bytes, str],
                         caption: str = None,
                         duration: int = None,
                         width: int = None,
                         height: int = None,
                         has_spoiler: bool = None,
                         parse_mode: ParseMode = ParseMode.NONE,
                         caption_entities: List['MessageEntity'] = None,
                         filename: str = None,
                         **kwargs
                         ) -> 'Message':
    """
    Sends an animation to a specified chat.

    :param animation: `Union[bytes, str]`
        The animation to be sent. It can be provided as bytes, a file path (str), or the file_id of an animation file
        that already exists on the Telegram servers.

    :param thumbnail: `Union[bytes, str]`
        The thumbnail of the animation. It should be provided as bytes or a file path.

    :param caption: `str`
        (Optional) A caption to accompany the animation.

    :param duration: `int`
        (Optional) Duration of the animation in seconds.

    :param width: `int`
        (Optional) Width of the animation in pixels.

    :param height: `int`
        (Optional) Height of the animation in pixels.

    :param has_spoiler: `bool`
        (Optional) Mark the animation as containing spoilers.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param filename: `str`
        (Optional) The filename to be used when sending the animation.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.

    :raises:
        :raise FileTooLargeError: If specified thumbnail is more than 200kB in size

    Notes:
        - Thumbnail can be ignored if thumbnail generation for the file is supported server-side.
          The thumbnail should be in JPEG format and less than 200 kB in size.
          A thumbnail's width and height should not exceed 320.
    """

    if isinstance(animation, str) and os.path.exists(animation):
        filename, animation = get_file(animation)
    if isinstance(thumbnail, str) and os.path.exists(thumbnail):
        _, thumbnail = get_file(thumbnail)

        if len(thumbnail) // 1024 > 200:
            raise FileTooLargeError(
                f"Specified thumbnail must be less than 200kB in size, got {len(thumbnail) // 1024}kB")

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None
    form_data = FormData()

    if thumbnail:
        form_data.add_field('thumbnail', thumbnail)
    form_data.add_field('animation', animation, filename=filename)

    return await send(
        method=APIMethod.SEND_ANIMATION,
        **exclude_from_dict(locals(), 'filename', 'kwargs', 'animation', "thumbnail"),
        **kwargs
    )


async def send_voice(voice: Union[bytes, str],
                     caption: str = None,
                     duration: int = None,
                     parse_mode: ParseMode = ParseMode.NONE,
                     caption_entities: List['MessageEntity'] = None,
                     **kwargs
                     ) -> 'Message':
    """
    Sends a voice message to a specified chat

    :param voice: `Union[bytes, str]`
        The voice message to be sent. It can be provided as bytes, a file path (str), or the file_id of a voice message
        that already exists on the Telegram servers.

    :param caption: `str`
        (Optional) A caption to accompany the voice message.

    :param duration: `int`
        (Optional) Duration of the voice message in seconds.

    :param parse_mode: `ParseMode`
        (Optional) The mode for parsing entities in the caption.
        Default is `ParseMode.NONE`.

    :param caption_entities: `List['MessageEntity']`
        (Optional) List of special entities in the caption.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    if isinstance(voice, str) and os.path.exists(voice):
        _, voice = get_file(voice)

    parse_mode = parse_mode.value
    caption_entities = MessageEntitySerializer().serialize(
        obj=caption_entities,
        many=True,
        keep_none_fields=False
    ) if caption_entities is not None else None

    return await send(
        method=APIMethod.SEND_VOICE,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def send_video_note(video_note: Union[bytes, str],
                          duration: int = None,
                          length: int = None,
                          **kwargs
                          ) -> 'Message':
    """
    Sends a video note (short video message) to a specified chat.

    :param video_note: `Union[bytes, str]`
        The video note to be sent. It can be provided as bytes, a file path (str), or the file_id of a video note
        that already exists on the Telegram servers.

    :param duration: `int`
        (Optional) Duration of the video note in seconds.

    :param length: `int`
        (Optional) Length of the video note in bytes.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    if isinstance(video_note, str) and os.path.exists(video_note):
        _, video_note = get_file(video_note)

    return await send(
        method=APIMethod.SEND_VIDEO_NOTE,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def send_poll(question: str,  # TODO: Errors (options length, ...)
                    options: List[str],
                    is_anonymous: bool = True,
                    type_: 'PollType' = None,
                    allows_multiple_answers: bool = None,
                    correct_option_id: int = None,
                    explanation: str = None,
                    explanation_parse_mode: ParseMode = ParseMode.NONE,
                    explanation_entities: List['MessageEntity'] = None,
                    open_period: int = None,
                    close_date: datetime = None,
                    is_closed: bool = None,
                    **kwargs
                    ) -> 'Message':
    """
    Send a poll to the specified chat.

    :param question: `str`
        The poll question.

    :param options: `List[str]`
        A list of options for the poll.

    :param is_anonymous: `bool`
        (Optional) If True, the poll will be anonymous.
        defaults to True

    :param type_: `PollType`
        (Optional) The type of poll to create.

    :param allows_multiple_answers: `bool`
        (Optional) If True, the poll allows multiple answers.

    :param correct_option_id: `int`
        (Optional) The index of the correct answer option (zero-based).

    :param explanation: `str`
        (Optional) Text that is shown when a user chooses an incorrect answer or taps on the lamp icon in a quiz-style poll,
        0-200 characters with at most 2 line feeds after entities parsing

    :param explanation_parse_mode: `ParseMode`
        (Optional) The parse mode of the explanation text.

    :param explanation_entities: `List[MessageEntity]`
        (Optional) A list of message entities in the explanation text.

    :param open_period: `int`
        (Optional) 	Amount of time in seconds the poll will be active after creation, 5-600.
        Can't be used together with close_date.

    :param close_date: `datetime`
        (Optional) Point in time (Unix timestamp) when the poll will be automatically closed.
        Must be at least 5 and no more than 600 seconds in the future. Can't be used together with open_period.

    :param is_closed: `bool`
        (Optional) Pass True if the poll needs to be immediately closed. This can be useful for poll preview.

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.

    :raises:
        :raise ValueError: If poll type is quiz and correct_option_id was not specified
    """
    from teleapi.types.poll.sub_object import PollType

    if type_ == PollType.QUIZ and correct_option_id is None:
        raise ValueError("Poll type is quiz and correct_option_id was not specified")

    explanation_parse_mode = explanation_parse_mode.value
    explanation_entities = MessageEntitySerializer().serialize(
        obj=explanation_entities,
        many=True,
        keep_none_fields=False
    ) if explanation_entities is not None else None
    close_date = close_date.timestamp() if close_date is not None else None
    type_ = type_.value if type_ is not None else None

    return await send(
        method=APIMethod.SEND_POLL,
        **exclude_from_dict(locals(), 'kwargs', 'type_'),
        **kwargs,
        type=type_
    )


async def send_contact(contact: 'Contact', **kwargs) -> 'Message':
    """
    Send a contact to the specified chat.

    :param contact: `Contact`
        The contact to be sent

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    contact = ContactSerializer().serialize(obj=contact, keep_none_fields=False)

    return await send(
        method=APIMethod.SEND_CONTACT,
        **exclude_from_dict(locals(), 'kwargs', 'contact'),
        **kwargs,
        **contact
    )


async def send_dice(emoji: str = None, **kwargs) -> 'Message':
    """
    Send the dice to the specified chat.

    :param emoji: `str`
        (Optional) Emoji on which the dice throw animation is based (see Dice model).
        Defaults to `🎲`

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    emoji = default(emoji, '🎲')

    return await send(
        method=APIMethod.SEND_DICE,
        **exclude_from_dict(locals(), 'kwargs'),
        **kwargs
    )


async def send_media_group(media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
                           **kwargs) -> List['Message']:
    """
    Sends a group of photos, videos, documents or audios as an album.
    Documents and audio files can be only grouped on an album with messages of the same type.
    On success, an array of Messages that were sent is returned.

    :param media: `list[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]`
        Media objects to be sent

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `List['Message']`
        The sent messages objects.

    :raises:
        :raise InvalidParameterError: If the length of provided media is less than 2 or gather than 10
        :raise ValueError: If media object has 'data' or 'thumbnail_data', but has no 'filename' or 'thumbnail_filename'
        :raise TypeError: If type grouping rules violated
    """

    if not (2 <= len(media) <= 10):
        raise InvalidParameterError(f"The length of provided media must be from 2 to 10")

    form_data = FormData()
    request_data = exclude_from_dict(locals(), 'kwargs', 'media')

    serialized_media = []

    media_types = [type(file) for file in media]

    if InputMediaDocument in media_types and any(
            (t in media_types for t in [InputMediaAudio, InputMediaPhoto, InputMediaVideo])):
        raise TypeError('Documents files can be only grouped on an album with messages of the same type')
    if InputMediaAudio in media_types and any(
            (t in media_types for t in [InputMediaDocument, InputMediaPhoto, InputMediaVideo])):
        raise TypeError('Audio files can be only grouped on an album with messages of the same type')

    for file in media:
        if file.data is not None:
            if file.filename is None:
                raise ValueError(f"filename was not specified")

            form_data.add_field(file.filename, file.data)

        if hasattr(file, 'thumbnail_data') and file.thumbnail_data is not None:
            if file.thumbnail_filename is None:
                raise ValueError(f"thumbnail_filename was not specified")

            form_data.add_field(file.thumbnail_filename, file.thumbnail_data)

        serialized_media.append(
            InputMediaObjectSerializer().serialize(obj=file, keep_none_fields=False)
        )

    return await send(
        method=APIMethod.SEND_MEDIA_GROUP,
        media=serialized_media,
        **request_data,
        **kwargs
    )


async def send_location(location: Location, **kwargs) -> 'Message':
    """
    Sends point on the map

    :param location: `Location`
        Location object to be sent

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    location_data = LocationSerializer().serialize(obj=location)

    return await send(
        method=APIMethod.SEND_DICE,
        **location_data,
        **kwargs,
    )


async def send_sticker(sticker: Union[str, bytes], emoji: str = None, **kwargs) -> 'Message':
    """
    Sends static .WEBP, animated .TGS, or video .WEBM stickers.

    :param sticker: `Union[str, bytes]`
        Sticker object to be sent

    :param emoji: `str`
        Emoji associated with the sticker; only for just uploaded stickers

    :param kwargs: `dict`
        Other parameters specified in `send` function above

    :return: `Message`
        The sent message object.
    """

    if isinstance(sticker, str) and os.path.exists(sticker):
        _, sticker = get_file(sticker)

    form_data = FormData()
    form_data.add_field('sticker', sticker)

    return await send(
        method=APIMethod.SEND_STICKER,
        **exclude_from_dict(locals(), 'kwargs', 'sticker'),
        **kwargs
    )
