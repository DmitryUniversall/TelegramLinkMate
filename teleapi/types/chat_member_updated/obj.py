from datetime import datetime

from .model import ChatMemberUpdatedModel


class ChatMemberUpdated(ChatMemberUpdatedModel):
    async def ban(self, until_date: datetime = None, revoke_messages: bool = None) -> bool:
        """
        Bans a member

        :param until_date: `datetime`
            (Optional) The date and time until which the ban will be active. If not provided, the ban will be permanent.
        :param revoke_messages: `bool`
            (Optional) Pass True to delete all messages from the chat for the user that is being removed

        :return: `bool`
            Returns True if the user was successfully banned

        :raises:
            :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        return await self.chat.ban_member(user=self.user, until_date=until_date, revoke_messages=revoke_messages)

    async def unban(self, only_if_banned: bool = None) -> bool:
        """
        Unbans a member

        :param only_if_banned: `bool`
            (Optional) Do nothing if the user is not banned

        :return: `bool`
            Returns True if the user was successfully unbanned

        :raises:
            :raise ApiRequestError: ApiRequestError or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
        """

        return await self.chat.unban_member(user=self.user, only_if_banned=only_if_banned)
