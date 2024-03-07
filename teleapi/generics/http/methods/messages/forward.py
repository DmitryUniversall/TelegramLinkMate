from typing import TYPE_CHECKING, List
from typing import Union
from teleapi.core.http.request.api_request import method_request
from teleapi.core.utils.collections import clear_none_values
from .utils import get_converted_reply_markup
from teleapi.types.forece_reply import ForceReply
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup
from teleapi.enums.parse_mode import ParseMode
from teleapi.types.message_entity import MessageEntity
from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup
from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
from teleapi.core.http.request.api_method import APIMethod

if TYPE_CHECKING:
    from teleapi.types.message import Message


async def forward_message(from_chat_id: int,
                          message_id: int,
                          to_chat_id: Union[int, str],
                          message_thread_id: int = None,
                          disable_notification: bool = None,
                          protect_content: bool = None
                          ) -> 'Message':
    from teleapi.types.message.serializer import MessageSerializer

    request_data = clear_none_values({
        "from_chat_id": from_chat_id,
        "chat_id": to_chat_id,
        "message_id": message_id,
        "message_thread_id": message_thread_id,
        "disable_notification": disable_notification,
        "protect_content": protect_content,
    })

    response, data = await method_request("POST", APIMethod.FORWARD_MESSAGE, data=request_data)

    return MessageSerializer().serialize(data=data['result'])


async def copy_message(to_chat_id: Union[int, str],
                       from_chat_id: int,
                       message_id: int,
                       disable_notification: bool = None,
                       protect_content: bool = None,
                       reply_to_message_id: int = None,
                       caption: str = None,
                       caption_entities: List[MessageEntity] = None,
                       parse_mode: ParseMode = ParseMode.NONE,
                       allow_sending_without_reply: bool = None,
                       reply_markup: Union[
                           'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                       ) -> int:
    reply_markup = await get_converted_reply_markup(reply_markup, None)

    request_data = clear_none_values({
        "chat_id": to_chat_id,
        "from_chat_id": from_chat_id,
        "reply_to_message_id": reply_to_message_id,
        "message_id": message_id,
        "parse_mode": parse_mode.value,
        "caption": caption,
        "disable_notification": disable_notification,
        "protect_content": protect_content,
        "allow_sending_without_reply": allow_sending_without_reply,
        "reply_markup": reply_markup,
        "caption_entities": caption_entities
    })

    response, data = await method_request("POST", APIMethod.COPY_MESSAGE, data=request_data)

    # noinspection PyTypeChecker
    return int(data['result']['message_id'])
