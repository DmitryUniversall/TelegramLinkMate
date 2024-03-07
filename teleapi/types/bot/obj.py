from typing import List, Union

from teleapi.core.exceptions.generics import InvalidParameterError
from teleapi.core.http.request import method_request, APIMethod
from teleapi.types.bot_command import TelegramBotCommand, TelegramBotCommandSerializer
from teleapi.types.bot.bot_description import BotDescription, BotDescriptionSerializer
from teleapi.types.bot_command_scope import TelegramBotCommandScope, BotCommandScopeObjectSerializer
from teleapi.types.chat_permissions.sub_objects.chat_administrator_rights import ChatAdministratorRights, ChatAdministratorRightsSerializer
from teleapi.types.menu_button import MenuButton
from teleapi.types.chat import Chat


class TelegramBotObject:
    async def set_commands(self, commands: List[TelegramBotCommand], scope: TelegramBotCommandScope = None, language_code: str = None) -> bool:
        """
        Changes the list of the bot commands. See this manual for more details about bot commands.

        :param commands: `List[TelegramBotCommand]`
            A list of bot commands to be set as the list of the bot commands. At most 100 commands can be specified.

        :param scope: `BotCommandScope`
            (Optional) A describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.

        :param language_code: `str`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated commands

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("post", APIMethod.SET_MY_COMMANDS, data={
            'commands': TelegramBotCommandSerializer().serialize(obj=commands, many=True),
            'scope': BotCommandScopeObjectSerializer().serialize(obj=scope),
            'language_code': language_code
        })

        return bool(data['result'])

    async def delete_commands(self, scope: TelegramBotCommandScope, language_code: str = None) -> bool:
        """
        Deletes the list of the bots commands for the given scope and user language.
        After deletion, higher level commands will be shown to affected users.

        :param scope: `BotCommandScope`
            A describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated commands

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("post", APIMethod.DELETE_MY_COMMANDS, data={
            'scope': BotCommandScopeObjectSerializer().serialize(obj=scope),
            'language_code': language_code
        })

        return bool(data['result'])

    async def get_commands(self, scope: TelegramBotCommandScope, language_code: str = None) -> List[TelegramBotCommandScope]:
        """
        Use this method to get the current list of the bots commands for the given scope and user language.
        Returns

        :param scope: `BotCommandScope`
            A describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code or an empty string

        :return: `List[TelegramBotCommandScope]`
            Returns an Array of BotCommand objects.
        """

        response, data = await method_request("get", APIMethod.GET_MY_COMMANDS, data={
            'scope': BotCommandScopeObjectSerializer().serialize(obj=scope),
            'language_code': language_code
        })

        return TelegramBotCommandSerializer().serialize(data=data["result"], many=True)

    async def set_name(self, name: str, language_code: str = None) -> bool:
        """
        Changes the bots name

        :param name: `str`
            New bot name; 0-64 characters. Pass an empty string to remove the dedicated name for the given language

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated name

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: if specified name is more than 64 characters long
        """

        if len(name) > 64:
            raise InvalidParameterError("Bots name must be <= 64 characters long")

        response, data = await method_request("get", APIMethod.SET_MY_NAME, data={
            'name': name,
            'language_code': language_code
        })

        return bool(data["result"])

    async def set_description(self, description: str, language_code: str = None) -> bool:
        """
        Changes the bots description, which is shown in the chat with the bot if the chat is empty

        :param description: `str`
            New bot description; 0-512 characters. Pass an empty string to remove the dedicated description for the given language

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated description

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: if specified description is more than 512 characters long
        """

        if len(description) > 512:
            raise InvalidParameterError("Bots description must be <= 512 characters long")

        response, data = await method_request("get", APIMethod.SET_MY_DESCRIPTION, data={
            'description': description,
            'language_code': language_code
        })

        return bool(data["result"])

    async def get_description(self, language_code: str = None) -> BotDescription:
        """
        Fetches the current bot description for the given user language

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated description

        :return: `bool`
            Returns BotDescription on success
        """

        response, data = await method_request("get", APIMethod.GET_MY_DESCRIPTION, data={
            'language_code': language_code
        })

        return BotDescriptionSerializer().serialize(data=data["result"])

    async def set_short_description(self, short_description: str, language_code: str = None) -> bool:
        """
        Changes the bots short description, which is shown on the bots profile page and is sent
        together with the link when users share the bot.

        :param short_description: `str`
            New short description for the bot; 0-120 characters.
            Pass an empty string to remove the dedicated short description for the given language.

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated short description

        :return: `bool`
            Returns True on success

        :raises:
            :raise InvalidParameterError: if bots short description is more than 120 characters long
        """

        if len(short_description) > 120:
            raise InvalidParameterError("Bots short description must be <= 120 characters long")

        response, data = await method_request("post", APIMethod.SET_MY_SHORT_DESCRIPTION, data={
            'short_description': short_description,
            'language_code': language_code
        })

        return bool(data["result"])

    async def get_short_description(self, language_code: str = None) -> BotDescription:
        """
        Fetches the current bot short description for the given user language

        :param language_code: `type`
             (Optional) A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope,
             for whose language there are no dedicated short description

        :return: `bool`
            Returns BotShortDescription on success
        """

        response, data = await method_request("get", APIMethod.GET_MY_SHORT_DESCRIPTION, data={
            'language_code': language_code
        })

        return BotDescriptionSerializer().serialize(data=data["result"])

    async def get_menu_button(self, chat: Union[Chat, int, str]) -> MenuButton:
        """
        Fetches the current value of the bots menu button in a private chat, or the default menu button
        (Alias for Chat.get_menu_button)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :return: `MenuButton`
            Returns MenuButton on success.
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.get_menu_button()

    async def set_default_administrator_rights(self, rights: ChatAdministratorRights = None, for_channels: bool = None) -> bool:
        """
        Changes the default administrator rights requested by the bot when it's added as an administrator to groups or channels.
        These rights will be suggested to users, but they are free to modify the list before adding the bot.

        :param rights: `ChatAdministratorRights`
            (Optional) New default administrator rights. If not specified, the default administrator rights will be cleared.

        :param for_channels: `bool`
            (Optional) Pass True to change the default administrator rights of the bot in channels.
            Otherwise, the default administrator rights of the bot for groups and supergroups will be changed

        :return: `bool`
            Returns True on success
        """

        response, data = await method_request("post", APIMethod.SET_MY_DEFAULT_ADMINISTRATOR_RIGHTS, data={
            'rights': ChatAdministratorRightsSerializer().serialize(obj=rights),
            'for_channels': for_channels
        })

        return bool(data["result"])

    async def get_default_administrator_rights(self, for_channels: bool = None) -> ChatAdministratorRights:
        """
        Fetches the current default administrator rights of the bot.

        :param for_channels: `bool`
            (Optional) Pass True to get default administrator rights of the bot in channels.
            Otherwise, default administrator rights of the bot for groups and supergroups will be returned.

        :return: `bool`
            Returns ChatAdministratorRights on success
        """

        response, data = await method_request("get", APIMethod.GET_MY_DEFAULT_ADMINISTRATOR_RIGHTS, data={
            'for_channels': for_channels
        })

        return ChatAdministratorRightsSerializer().serialize(data=data['result'])
