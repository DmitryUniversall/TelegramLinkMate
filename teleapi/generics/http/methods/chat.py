from typing import Union, TYPE_CHECKING
from datetime import datetime
from teleapi.core.exceptions.generics import InvalidParameterError
from teleapi.core.http.request import method_request, APIMethod

if TYPE_CHECKING:
    from teleapi.types.chat_invite_link import ChatInviteLink


async def edit_invite_link(chat_id: Union[int, str],
                           invite_link: str,
                           name: str = None,
                           expire_date: datetime = None,
                           member_limit: int = None,
                           creates_join_request: bool = None) -> 'ChatInviteLink':
    """
    Edit a non-primary invite link created by the bot.
    The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights

    :param chat_id: `Union[int, str]`
        The chat ID or username

    :param invite_link: `str`
        The invite link to edit

    :param name: `str`
        Invite link name; 0-32 characters

    :param expire_date: `datetime`
        Point in time when the link will expire

    :param member_limit: `int`
        The maximum number of users that can be members of the chat
        simultaneously after joining the chat via this invite link; 1-99999

    :param creates_join_request: `bool`
        True, if users joining the chat via the link need to be approved by chat administrators.
        If True, member_limit can't be specified

    :return: `ChatInviteLink`
        Edited invite link

    :raises:
        :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        :raise InvalidParameterError: If the provided name is more than 30 characters long
    """

    from teleapi.types.chat_invite_link import ChatInviteLinkSerializer

    if len(name) > 30:
        raise InvalidParameterError("Link name must be <= 30 characters long")

    expire_date = expire_date.timestamp() if expire_date is not None else None

    response, data = await method_request("post", APIMethod.EDIT_CHAT_INVITE_LINK, data=locals())

    return ChatInviteLinkSerializer().serialize(data=data)


async def revoke_chat_invite_link(chat_id: Union[int, str], invite_link: str) -> 'ChatInviteLink':
    """
    Revoke an invite link created by the bot.
    If the primary link is revoked, a new link is automatically generated.
    The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights.

    :param chat_id: `Union[int, str, 'Chat']`
        The chat ID, username or Chat object of the chat to be unbanned.

    :param invite_link: `str`
        The invite link to revoke

    :return: `ChatInviteLink`
        The revoked invite link

    :raises:
        :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
        :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        :raise ValidationError: If the provided data model contains incorrect data or serialization failed
    """

    from teleapi.types.chat_invite_link import ChatInviteLinkSerializer

    response, data = await method_request("post", APIMethod.REVOKE_CHAT_INVITE_LINK, data=locals())

    return ChatInviteLinkSerializer().serialize(data=data)
