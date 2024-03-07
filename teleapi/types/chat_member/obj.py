from datetime import datetime
from typing import Union

from teleapi.types.chat import Chat
from teleapi.types.chat_permissions import ChatPermissions
from .model import ChatMemberModel


class ChatMember(ChatMemberModel):
    async def restrict(self,
                       chat: Union[Chat, int, str],
                       permissions: ChatPermissions,
                       use_independent_chat_permissions: bool = None,
                       until_date: datetime = None) -> bool:
        """
        Restricts specified member
        (Alias for Chat.restrict_member)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param permissions: `ChatPermissions`
            New user permissions

        :param use_independent_chat_permissions: `bool`
            (Optional) Pass True if chat permissions are set independently.
            Otherwise, the can_send_other_messages and can_add_web_page_previews permissions
            will imply the can_send_messages, can_send_audios, can_send_documents,
            can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions;
            the can_send_polls permission will imply the can_send_messages permission.

        :param until_date: `datetime`
            (Optional) Date when restrictions will be lifted for the user, unix time.
            If user is restricted for more than 366 days or less than 30 seconds from the current time,
            they are considered to be restricted forever

        :return: `bool`
            Returns True on success
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.restrict_member(
            user=self.user,
            permissions=permissions,
            use_independent_chat_permissions=use_independent_chat_permissions,
            until_date=until_date
        )

    async def promote_member(self,
                             chat: Union[Chat, int, str],
                             is_anonymous: bool = None,
                             can_manage_chat: bool = None,
                             can_post_messages: bool = None,
                             can_edit_messages: bool = None,
                             can_delete_messages: bool = None,
                             can_manage_video_chats: bool = None,
                             can_restrict_members: bool = None,
                             can_promote_members: bool = None,
                             can_change_info: bool = None,
                             can_invite_users: bool = None,
                             can_pin_messages: bool = None,
                             can_manage_topics: bool = None,
                             ) -> bool:
        """
        Promote a member to an administrator in the chat with specified privileges.
        (Alias for Chat.promote_member)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param is_anonymous: `bool`
            (Optional) Pass True if the promoted administrator's actions should be shown as anonymous in the chat.

        :param can_manage_chat: `bool`
            (Optional) Pass True if the administrator can access the chat event log, chat statistics, message statistics
            in channels, see channel members, see anonymous administrators in supergroups, and ignore slow mode.
            Implied by any other administrator privilege.

        :param can_post_messages: `bool`
            (Optional) Pass True if the administrator can create channel posts. (Channels only)

        :param can_edit_messages: `bool`
            (Optional) Pass True if the administrator can edit messages of other users and can pin messages. (Channels only)

        :param can_delete_messages: `bool`
            (Optional) Pass True if the administrator can delete messages of other users.

        :param can_manage_video_chats: `bool`
            (Optional) Pass True if the administrator can manage video chats.

        :param can_restrict_members: `bool`
            (Optional) Pass True if the administrator can restrict, ban, or unban chat members.

        :param can_promote_members: `bool`
            (Optional) Pass True if the administrator can add new administrators with a subset of their own privileges or
            demote administrators that they have promoted,
            directly or indirectly (promoted by administrators that were appointed by them).

        :param can_change_info: `bool`
            (Optional) Pass True if the administrator can change chat title, photo, and other settings.

        :param can_invite_users: `bool`
            (Optional) Pass True if the administrator can invite new users to the chat.

        :param can_pin_messages: `bool`
            (Optional) Pass True if the administrator can pin messages. (Supergroups only)

        :param can_manage_topics: `bool`
            (Optional) Pass True if the user is allowed to create, rename, close, and reopen forum topics. (Supergroups only)

        :return: `bool`
            Returns True if the member was successfully promoted
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.promote_member(
            user=self.user,
            is_anonymous=is_anonymous,
            can_manage_chat=can_manage_chat,
            can_post_messages=can_post_messages,
            can_edit_messages=can_edit_messages,
            can_delete_messages=can_delete_messages,
            can_manage_video_chats=can_manage_video_chats,
            can_restrict_members=can_restrict_members,
            can_promote_members=can_promote_members,
            can_change_info=can_change_info,
            can_invite_users=can_invite_users,
            can_pin_messages=can_pin_messages,
            can_manage_topics=can_manage_topics
        )

    async def ban(self,
                  chat: Union[Chat, int, str],
                  until_date: datetime = None,
                  revoke_messages: bool = None
                  ) -> bool:
        """
        Bans a member
        (Alias for Chat.ban_member)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param until_date: `datetime`
            (Optional) The date and time until which the ban will be active. If not provided, the ban will be permanent.

        :param revoke_messages: `bool`
            (Optional) Pass True to delete all messages from the chat for the user that is being removed

        :return: `bool`
            Returns True if the user was successfully banned
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.ban_member(
            user=self.user,
            until_date=until_date,
            revoke_messages=revoke_messages
        )

    async def unban(self,
                    chat: Union[Chat, int, str],
                    only_if_banned: bool = None
                    ) -> bool:
        """
        Unbans a member
        (Alias for Chat.unban_member)

        :param chat: `Union[Chat, int]`
            Chat in which you need to install custom title.
            if `int | str` - will be fetched using id

        :param only_if_banned: `bool`
            (Optional) Do nothing if the user is not banned

        :return: `bool`
            Returns True if the user was successfully unbanned
        """

        if not isinstance(chat, Chat):
            chat = await Chat.get_chat(chat)

        return await chat.unban_member(
            user=self.user,
            only_if_banned=only_if_banned
        )
