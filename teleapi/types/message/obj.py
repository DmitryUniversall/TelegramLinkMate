import asyncio
import logging
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union, List

from teleapi.enums.parse_mode import ParseMode
from .exceptions import MessageTooOld, MessageTooNew, MessageIsNotModified, MessageHasNoMedia
from .model import MessageModel
from ..chat.chat_type import ChatType
from ..contact import Contact
from ..input_media.sub_objects.audio import InputMediaAudio
from ..input_media.sub_objects.document import InputMediaDocument
from ..input_media.sub_objects.photo import InputMediaPhoto
from ..input_media.sub_objects.video import InputMediaVideo
from ..location import Location
from ..poll.sub_object import PollType
from ..poll import Poll
from ...core.exceptions.generics import InvalidParameterError
from ...core.utils.collections import exclude_from_dict
from ...core.utils.syntax import default

if TYPE_CHECKING:
    from ..inline_keyboard_markup import InlineKeyboardMarkup
    from ..reply_keyboard_markup.obj import ReplyKeyboardMarkup
    from ..reply_keyboard_markup.sub_objects.keyboard_remove import ReplyKeyboardRemove
    from ...core.ui.inline_view import BaseInlineView
    from ..forece_reply import ForceReply
    from ..message_entity import MessageEntity
    from ..chat.obj import Chat

logger = logging.getLogger(__name__)


class Message(MessageModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, Message) and other.id == self.id

    async def reply(self,
                    text: str,
                    parse_mode: ParseMode = ParseMode.NONE,
                    disable_web_page_preview: bool = None,
                    disable_notification: bool = None,
                    protect_content: bool = None,
                    allow_sending_without_reply: bool = None,
                    view: 'BaseInlineView' = None,
                    reply_markup: Union[
                        'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                    ) -> 'Message':

        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_message(**payload)

    async def reply_photo(self,
                          photo: Union[bytes, str],
                          caption: str = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          has_spoiler: bool = None,
                          disable_notification: bool = None,
                          protect_content: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_photo(**payload)

    async def reply_audio(self,
                          audio: Union[bytes, str],
                          caption: str = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          duration: int = None,
                          performer: str = None,
                          title: str = None,
                          thumbnail: Union[bytes, str] = None,
                          disable_notification: bool = None,
                          protect_content: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_audio(**payload)

    async def reply_document(self,
                             document: Union[bytes, str],
                             caption: str = None,
                             parse_mode: ParseMode = ParseMode.NONE,
                             caption_entities: List['MessageEntity'] = None,
                             disable_content_type_detection: bool = None,
                             thumbnail: Union[bytes, str] = None,
                             disable_notification: bool = None,
                             protect_content: bool = None,
                             allow_sending_without_reply: bool = None,
                             view: 'BaseInlineView' = None,
                             filename: str = None,
                             reply_markup: Union[
                                 'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                             ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_document(**payload)

    async def reply_video(self,
                          video: Union[bytes, str],
                          thumbnail: Union[bytes, str] = None,
                          caption: str = None,
                          duration: int = None,
                          height: int = None,
                          width: int = None,
                          has_spoiler: bool = None,
                          supports_streaming: bool = None,
                          parse_mode: ParseMode = ParseMode.NONE,
                          caption_entities: List['MessageEntity'] = None,
                          disable_notification: bool = None,
                          allow_sending_without_reply: bool = None,
                          view: 'BaseInlineView' = None,
                          filename: str = None,
                          reply_markup: Union[
                              'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                          ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_video(**payload)

    async def reply_video_note(self,
                               video_note: Union[bytes, str],
                               duration: int = None,
                               length: int = None,
                               protect_content: bool = None,
                               disable_notification: bool = None,
                               allow_sending_without_reply: bool = None,
                               reply_markup: Union[
                                   'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                               view: 'BaseInlineView' = None
                               ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_video_note(**payload)

    async def reply_poll(self,
                         question: str,
                         options: List[str] = None,
                         is_anonymous: bool = None,
                         type_: PollType = None,
                         allows_multiple_answers: bool = None,
                         correct_option_id: int = None,
                         explanation: str = None,
                         explanation_parse_mode: ParseMode = ParseMode.NONE,
                         explanation_entities: List['MessageEntity'] = None,
                         open_period: int = None,
                         close_date: datetime = None,
                         is_closed: bool = None,
                         disable_notification: bool = None,
                         protect_content: bool = None,
                         allow_sending_without_reply: bool = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         view: 'BaseInlineView' = None
                         ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_poll(**payload)

    async def reply_contact(self,
                            contact: 'Contact',
                            disable_notification: bool = None,
                            protect_content: bool = None,
                            allow_sending_without_reply: bool = None,
                            reply_markup: Union[
                                'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                            view: 'BaseInlineView' = None
                            ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_contact(**payload)

    async def reply_dice(self,
                         emoji: 'str' = None,
                         disable_notification: bool = None,
                         protect_content: bool = None,
                         allow_sending_without_reply: bool = None,
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         view: 'BaseInlineView' = None
                         ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_dice(**payload)

    async def reply_media_group(self,
                                media: List[
                                    Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
                                disable_notification: bool = None,
                                protect_content: bool = None,
                                allow_sending_without_reply: bool = None,
                                reply_markup: Union[
                                    'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                view: 'BaseInlineView' = None
                                ) -> List['Message']:
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_media_group(**payload)

    async def reply_animation(self,
                              animation: Union[bytes, str],
                              thumbnail: Union[bytes, str] = None,
                              caption: str = None,
                              duration: int = None,
                              width: int = None,
                              height: int = None,
                              has_spoiler: bool = None,
                              parse_mode: ParseMode = ParseMode.NONE,
                              caption_entities: List['MessageEntity'] = None,
                              filename: str = None,
                              disable_notification: bool = None,
                              protect_content: bool = None,
                              allow_sending_without_reply: bool = None,
                              reply_markup: Union[
                                  'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                              view: 'BaseInlineView' = None
                              ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_animation(**payload)

    async def send_location(self,
                            location: Location,
                            disable_notification: bool = None,
                            protect_content: bool = None,
                            allow_sending_without_reply: bool = None,
                            reply_markup: Union[
                                'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                            view: 'BaseInlineView' = None
                            ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['reply_to_message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.send_location(**payload)

    async def forward(self,
                      to_chat: Union['Chat', int, str],
                      disable_notification: bool = None,
                      protect_content: bool = None
                      ) -> 'Message':
        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self
        payload['message_thread_id'] = self.thread_id

        return await self.chat.forward_message(**payload)

    async def edit_text(self,
                        text: str,
                        parse_mode: ParseMode = ParseMode.NONE,
                        disable_web_page_preview: bool = None,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None,
                        keep_reply_markup: bool = False,
                        entities: List['MessageEntity'] = None
                        ) -> Union['Message', bool]:
        if keep_reply_markup:
            if not self.reply_markup:
                logger.warning(
                    f"reply_markup argument is specified in Message.edit_text call, but message ({self.id}) object have no 'reply_markup' attribute defined before")
            else:
                reply_markup = self.reply_markup

        if self.text == text and self.reply_markup == reply_markup:
            raise MessageIsNotModified("Specified content and reply markup are exactly the same as a current")

        payload = exclude_from_dict(locals(), 'self', 'keep_reply_markup')
        payload['message'] = self

        result = await self.chat.edit_message_text(**payload)

        self.text = text
        self.reply_markup = reply_markup
        self.entities = entities

        return result

    async def edit_caption(self,
                           caption: str,
                           parse_mode: ParseMode = ParseMode.NONE,
                           caption_entities: List['MessageEntity'] = None,
                           reply_markup: Union[
                               'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                           view: 'BaseInlineView' = None,
                           keep_reply_markup: bool = False
                           ) -> Union['Message', bool]:
        if keep_reply_markup:
            if not self.reply_markup:
                logger.warning(
                    f"reply_markup argument is specified in Message.edit_caption call, but message ({self.id}) object have no 'reply_markup' attribute defined before")
            else:
                reply_markup = self.reply_markup

        if self.caption == caption and self.reply_markup == reply_markup:
            raise MessageIsNotModified("Specified content and reply markup are exactly the same as a current")

        payload = exclude_from_dict(locals(), 'self', 'keep_reply_markup')
        payload['message'] = self

        result = await self.chat.edit_message_caption(**payload)

        self.caption = caption
        self.caption_entities = caption_entities

        return result

    async def edit_media(self,
                         media: Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo],
                         reply_markup: Union[
                             'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                         view: 'BaseInlineView' = None,
                         keep_reply_markup: bool = False
                         ) -> Union['Message', bool]:
        if keep_reply_markup:
            if not self.reply_markup:
                logger.warning(
                    f"reply_markup argument is specified in Message.edit_caption call, but message ({self.id}) object have no 'reply_markup' attribute defined before")
            else:
                reply_markup = self.reply_markup

        if not any((self.photo, self.animation, self.document, self.audio, self.video)):
            raise MessageHasNoMedia("Message has no media to be modified")

        payload = exclude_from_dict(locals(), 'self', 'keep_reply_markup')
        payload['message'] = self

        result = await self.chat.edit_message_media(**payload)

        # TODO: Edit this message object

        return result

    async def edit_reply_markup(self,
                                reply_markup: Union[
                                    'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                view: 'BaseInlineView' = None
                                ) -> Union['Message', bool]:

        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self

        result = await self.chat.edit_message_reply_markup(**payload)

        self.reply_markup = reply_markup

        return result

    async def edit_live_location(self,
                                 location: Location,
                                 reply_markup: Union[
                                     'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                 view: 'BaseInlineView' = None
                                 ) -> Union['Message', bool]:

        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self

        result = await self.chat.edit_message_live_location(**payload)

        self.location = location

        return result

    async def stop_live_location(self,
                                 reply_markup: Union[
                                     'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                                 view: 'BaseInlineView' = None
                                 ) -> Union['Message', bool]:

        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self

        result = await self.chat.stop_message_live_location(**payload)

        self.location = None

        return result

    async def stop_poll(self,
                        reply_markup: Union[
                            'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None,
                        view: 'BaseInlineView' = None
                        ) -> Poll:

        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self

        result = await self.chat.stop_poll(**payload)

        self.poll = result

        return result

    async def copy(self,
                   to_chat: Union['Chat', int, str],
                   disable_notification: bool = None,
                   protect_content: bool = None,
                   reply_to_message: Union[int, 'Message'] = None,
                   caption: str = None,
                   caption_entities: List['MessageEntity'] = None,
                   parse_mode: ParseMode = ParseMode.NONE,
                   allow_sending_without_reply: bool = None,
                   reply_markup: Union[
                       'InlineKeyboardMarkup', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ForceReply', dict] = None
                   ) -> int:
        payload = exclude_from_dict(locals(), 'self')
        payload['message'] = self
        payload['reply_to_message'] = reply_to_message if isinstance(reply_to_message,
                                                                     int) or reply_to_message is None else reply_to_message.id
        payload['caption'] = default(caption, self.caption)
        payload['caption_entities'] = default(caption_entities, self.caption_entities)
        payload['reply_markup'] = default(reply_markup, self.reply_markup)
        payload['message_thread_id'] = self.thread_id

        return await self.chat.copy_message(**payload)

    async def pin(self, disable_notification: bool = None) -> bool:
        """
        Adds a message to the list of pinned messages in a chat.
        If the chat is not a private chat, the bot must be an administrator in the chat for this to work and
        must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages'
        administrator right in a channel.

        :param disable_notification: `bool`
            (Optional) Sends the message silently. Users will receive a notification with no sound.

        :return: `bool`
            Returns true on success
        """

        return await self.chat.pin_message(
            message=self,
            disable_notification=disable_notification
        )

    async def unpin(self) -> bool:
        """
        Removes a message from the list of pinned messages in a chat.
        If the chat is not a private chat, the bot must be an administrator in the chat for this to work and
        must have the 'can_pin_messages' administrator right in a supergroup or 'can_edit_messages'
        administrator right in a channel.

        :return: `bool`
            Returns true on success
        """

        return await self.chat.unpin_message(
            message=self,
        )

    async def delete(self, delete_after: int = None) -> bool:
        """
        Deletes this message

        :param delete_after: `int`
            (Optional) The time in seconds to wait before deleting the message

        :return: `bool`
            Returns True on success

        :raises:
            :raise MessageTooOld: if message is too old to be deleted (see Notes)
            :rise InvalidParameterError: if delete_after is longer than 48 hours (A message can only be deleted if it was sent less than 48 hours ago)

        Notes:
         - A message can only be deleted if it was sent less than 48 hours ago.
         - A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.
         - Service messages about a supergroup, channel, or forum topic creation can't be deleted.
         - Bots can delete outgoing messages in private chats, groups, and supergroups.
         - Bots can delete incoming messages in private chats.
         - Bots granted can_post_messages permissions can delete outgoing messages in channels.
         - If the bot is an administrator of a group, it can delete any message there.
         - If the bot has can_delete_messages permission in a supergroup or a channel, it can delete any message there.
        """

        if delete_after is not None and delete_after > timedelta(hours=48).total_seconds():
            raise InvalidParameterError("Message can not be deleted after 48 hours")

        if delete_after:
            await asyncio.sleep(delete_after)

        message_time_delta = datetime.now() - self.date

        if message_time_delta > timedelta(hours=48):
            raise MessageTooOld("A message can only be deleted if it was sent less than 48 hours ago.")
        elif self.dice is not None and self.chat.type_ == ChatType.PRIVATE and message_time_delta < timedelta(hours=24):
            raise MessageTooNew(
                "A dice message in a private chat can only be deleted if it was sent more than 24 hours ago.")

        return await self.chat.delete_message(message=self)
