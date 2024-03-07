from enum import Enum


class UpdateEvent(Enum):
    ON_MESSAGE = "on_message"
    ON_CHANNEL_POST = 'ON_CHANNEL_POST'
    ON_COMMAND = "on_command"
    ON_CALLBACK_QUERY = "on_callback_query"
    ON_CHAT_MEMBER_UPDATED = "on_chat_member_updated"
    ON_BOT_CHAT_MEMBER_UPDATED = "on_bot_chat_member_updated"
    ON_POLL_STATUS_UPDATED = "on_poll_status_updated"
    ON_POLL_ANSWER = "on_poll_answer"
    ON_CHAT_JOIN_REQUEST = "on_chat_join_request"


class AllowedUpdates(Enum):
    MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    CHANNEL_POST = "channel_post"
    EDITED_CHANNEL_POST = "edited_channel_post"
    INLINE_QUERY = "inline_query"
    CHOSEN_INLINE_RESULT = "chosen_inline_result"
    CALLBACK_QUERY = "callback_query"
    SHIPPING_QUERY = "shipping_query"
    PRE_CHECKOUT_QUERY = "pre_checkout_query"
    POLL = "poll"
    POLL_ANSWER = "poll_answer"
    MY_CHAT_MEMBER = "my_chat_member"
    CHAT_MEMBER = "chat_member"
    CHAT_JOIN_REQUEST = "chat_join_request"


AllowedUpdates_default = [AllowedUpdates.MESSAGE, AllowedUpdates.EDITED_MESSAGE, AllowedUpdates.CHANNEL_POST,
                          AllowedUpdates.EDITED_CHANNEL_POST, AllowedUpdates.INLINE_QUERY,
                          AllowedUpdates.CHOSEN_INLINE_RESULT, AllowedUpdates.CALLBACK_QUERY,
                          AllowedUpdates.SHIPPING_QUERY, AllowedUpdates.PRE_CHECKOUT_QUERY, AllowedUpdates.POLL,
                          AllowedUpdates.POLL_ANSWER, AllowedUpdates.CHAT_JOIN_REQUEST]

AllowedUpdates_all = list(AllowedUpdates)
