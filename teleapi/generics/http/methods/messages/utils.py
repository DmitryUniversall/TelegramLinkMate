from typing import Union, TYPE_CHECKING
from teleapi.types.forece_reply import ForceReply, ForceReplySerializer
from teleapi.types.inline_keyboard_markup import InlineKeyboardMarkup, InlineKeyboardMarkupSerializer
from teleapi.types.reply_keyboard_markup import ReplyKeyboardMarkup, ReplyKeyboardMarkupSerializer
from teleapi.types.reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove, ReplyKeyboardRemoveSerializer

if TYPE_CHECKING:
    from teleapi.core.ui.inline_view import BaseInlineView

reply_markup_mapping = {
    InlineKeyboardMarkup: InlineKeyboardMarkupSerializer,
    ReplyKeyboardMarkup: ReplyKeyboardMarkupSerializer,
    ReplyKeyboardRemove: ReplyKeyboardRemoveSerializer,
    ForceReply: ForceReplySerializer
}


async def get_converted_reply_markup(
        reply_markup: Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict],
        view: 'BaseInlineView' = None) -> dict:
    if view:
        markup = await view.make_markup()
        reply_markup = InlineKeyboardMarkupSerializer().serialize(obj=markup, keep_none_fields=False)

    if reply_markup is not None and not isinstance(reply_markup, dict):
        serializer = reply_markup_mapping.get(type(reply_markup))
        if serializer is None:
            raise TypeError("Unknown reply_markup type: {type(reply_markup)}")

        reply_markup = serializer().serialize(obj=reply_markup, keep_none_fields=False)

    return reply_markup
