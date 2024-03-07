from typing import Optional

from teleapi.core.orm.models import Model
from teleapi.core.orm.models.generics.fields import IntegerModelField
from teleapi.core.orm.models.generics.fields import RelatedModelField
from teleapi.types.chat_join_request import ChatJoinRequest
from teleapi.types.chat_member_updated import ChatMemberUpdated
from teleapi.types.message.obj import Message
from teleapi.types.callback_query import CallbackQuery
from teleapi.types.poll import Poll
from teleapi.types.poll.sub_object.answer import PollAnswer


class UpdateModel(Model):
    id: int = IntegerModelField()
    message: Optional[Message] = RelatedModelField(Message, is_required=False)
    edited_message: Optional[Message] = RelatedModelField(Message, is_required=False)
    channel_post: Optional[Message] = RelatedModelField(Message, is_required=False)
    edited_channel_post: Optional[Message] = RelatedModelField(Message, is_required=False)
    callback_query: Optional[CallbackQuery] = RelatedModelField(CallbackQuery, is_required=False)
    bot_chat_member: Optional[ChatMemberUpdated] = RelatedModelField(ChatMemberUpdated, is_required=False)
    chat_member: Optional[ChatMemberUpdated] = RelatedModelField(ChatMemberUpdated, is_required=False)
    poll: Optional[Poll] = RelatedModelField(Poll, is_required=False)
    poll_answer: Optional[PollAnswer] = RelatedModelField(PollAnswer, is_required=False)
    chat_join_request: Optional[ChatJoinRequest] = RelatedModelField(ChatJoinRequest, is_required=False)

    # inline_query: Optional[InlineQuery] = RelatedModelField(InlineQuery, is_required=False)
    # chosen_inline_result: Optional[ChosenInlineResult] = RelatedModelField(ChosenInlineResult, is_required=False)
    # shipping_query: Optional[ShippingQuery] = RelatedModelField(ShippingQuery, is_required=False)
    # pre_checkout_query: Optional[PreCheckoutQuery] = RelatedModelField(PreCheckoutQuery, is_required=False)
