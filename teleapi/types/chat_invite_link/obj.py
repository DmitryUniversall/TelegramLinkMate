from datetime import datetime
from typing import Union, TYPE_CHECKING
from .model import ChatInviteLinkModel
from teleapi.generics.http.methods.chat import revoke_chat_invite_link, edit_invite_link
from ...core.utils.collections import exclude_from_dict

if TYPE_CHECKING:
    from ..chat import Chat


class ChatInviteLink(ChatInviteLinkModel):
    async def edit(self,
                   chat: Union[int, str, 'Chat'],
                   name: str = None,
                   expire_date: datetime = None,
                   member_limit: int = None,
                   creates_join_request: bool = None) -> 'ChatInviteLink':
        """
        Edit a non-primary invite link created by the bot.
        The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights

        :param chat: `Union[int, str, 'Chat']`
            The chat ID, username or Chat object of what invite link belongs to

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
        """

        return await edit_invite_link(
            chat_id=chat if isinstance(chat, (int, str)) else chat.id,
            invite_link=self.invite_link,
            **exclude_from_dict(locals(), 'self', 'chat')
        )

    async def revoke(self, chat: Union[int, str, 'Chat']) -> 'ChatInviteLink':
        """
        Revoke an invite link created by the bot.
        If the primary link is revoked, a new link is automatically generated.
        The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights.

        :param chat: `Union[int, str, 'Chat']`
            The chat ID, username or Chat object of what invite link belongs to

        :return: `ChatInviteLink`
            The revoked invite link

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        return await revoke_chat_invite_link(
            chat_id=chat if isinstance(chat, (int, str)) else chat.id,
            invite_link=self.invite_link
        )
