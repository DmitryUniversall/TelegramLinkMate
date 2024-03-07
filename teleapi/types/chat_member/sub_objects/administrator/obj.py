from typing import Union

from teleapi.types.chat import Chat
from teleapi.types.chat_member import ChatMember
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRights
from .model import ChatAdministratorModel


class ChatAdministrator(ChatAdministratorModel, ChatAdministratorRights, ChatMember):
    async def set_custom_title(self, chat: Union[Chat, int, str], custom_title: str) -> bool:
        """
        Set a custom title for an administrator in a supergroup promoted by the bot
        (Alias for Chat.set_administrator_custom_title)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param custom_title: `type`
            New custom title for the administrator; 0-16 characters, emoji are not allowed

        :return: `bool`
            Returns True on success
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.set_administrator_custom_title(
            user=self.user,
            custom_title=custom_title
        )
