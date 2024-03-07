from .model import ChatJoinRequestModel


class ChatJoinRequest(ChatJoinRequestModel):
    async def approve(self) -> bool:
        """
        Approves a chat join request.
        The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right.

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        return await self.chat.approve_join_request(user=self.user)

    async def decline(self) -> bool:
        """
        Declines a chat join request.
        The bot must be an administrator in the chat for this to work and must have the can_invite_users administrator right.

        :return: `bool`
            Returns True on success

        :raises:
            :raise ApiRequestError: or any of its subclasses if the request sent to the Telegram Bot API fails.
            :raise aiohttp.ClientError: If there's an issue with the HTTP request itself.
            :raise ValidationError: If the provided data model contains incorrect data or serialization failed
        """

        return await self.chat.decline_join_request(user=self.user)
