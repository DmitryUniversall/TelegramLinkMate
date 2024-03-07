from typing import Union, TYPE_CHECKING

from teleapi.types.chat import Chat
from .exceptions import BadPollState
from .model import PollModel
from ..reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove

if TYPE_CHECKING:
    from ...core.ui.inline_view.view import BaseInlineView
    from ..forece_reply import ForceReply
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..reply_keyboard_markup import ReplyKeyboardMarkup
    from ..reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from teleapi.types.message import Message


class Poll(PollModel):
    async def stop(self,
                   chat: Union[int, str, Chat],
                   message: Union['Message', int],
                   reply_markup: Union[
                       'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                   view: 'BaseInlineView' = None) -> 'Poll':
        """
        Stop a poll which was sent by the bot.
        (Alias for chat.stop_poll)

        :param chat: `Union[Chat, str, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param message: `Union[Message, int]`
            Identifier of the message to edit or Message object

        :param reply_markup: `Union['InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict]`
            (Optional) Additional interface for the message.

        :param view: `BaseInlineView`
            (Optional) Inline view to control message interface.

        :return: `Poll`
            On success, the stopped Poll is returned.

        :raises:
            :raise BadPollState: If poll is already stopped
        """

        if self.is_closed:
            raise BadPollState("Poll is already stopped")

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.stop_poll(
            message=message,
            reply_markup=reply_markup,
            view=view
        )
