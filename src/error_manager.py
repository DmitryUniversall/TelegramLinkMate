import os.path
import random

import teleapi
from .exceptions.exceptions import UserError
from .utils.text import strip_lines
from teleapi.generics.http.methods.messages.send import send_media_group, send_message
import pickle


def get_error_message_text(text: str) -> str:
    return strip_lines(
        f"""
        ⚠️ <b>Произошла ошибка</b>:
        Подробности: <i>{text}</i>
        """
    )


def get_unknown_error_message_text() -> str:
    return strip_lines(
        """
        ⚠️ <b>Произошла неизвестная ошибка:</b>
        При обработке команды произошла непредвиденная ошибка.
        Пожалуйста, попробуйте ещё раз позже или сообщите об ошибке администратору с помощью кнопки ниже.
        """
    )


class UnknownErrorMessageView(teleapi.View):
    def __init__(self, error_id: int, error: Exception, update: teleapi.Update) -> None:
        super().__init__()

        self.error_id = error_id
        self.error = error
        self.update = update

    @teleapi.View.view_button(text="📢 Сообщить об ошибке", row=0)
    async def report_button(self, callback_query: teleapi.CallbackQuery, button: teleapi.InlineViewButton) -> None:
        await send_message(
            chat_id=teleapi.project_settings.OWNER_CHAT_ID,
            text=f"<b>New error report for {self.error_id} (on update {self.update.id}) from <em>{callback_query.user.username}</em></b>:\n\n<em>{str(self.error)}</em>",
            parse_mode=teleapi.ParseMode.HTML
        )

        await callback_query.answer("Спасибо за сообщение об ошибке. Мы постараемся её исправить")

        self.unregister_button(button)
        await self.message.edit_reply_markup(view=self)


class BotErrorManager(teleapi.ErrorManager):
    @teleapi.ErrorManager.manager_handler(exception_cls=UserError)
    async def user_error_handler(self, error: Exception, update: teleapi.Update, **_) -> bool:
        if not update.message:
            return False

        await update.message.reply(
            text=get_error_message_text(str(error)),
            parse_mode=teleapi.ParseMode.HTML
        )

        return True

    async def handle_unknown_error(self, error: Exception, update: teleapi.Update) -> None:
        await super().handle_unknown_error(error, update)

        error_id = random.randint(1000, 1000000)

        await send_media_group(
            chat_id=teleapi.project_settings.OWNER_CHAT_ID,
            media=[
                teleapi.InputMediaDocument(
                    data=pickle.dumps(error),
                    filename="error_object.pkl"
                ),
                teleapi.InputMediaDocument(
                    data=pickle.dumps(update),
                    filename="update_object.pkl"
                ),
                teleapi.InputMediaDocument(
                    media=os.path.join(teleapi.project_settings.PROCESS_LOG_DIR, "debug.log"),
                    filename="recent_logs.log",
                    caption=f"<b>Unknown error ({error_id}) occurred:</b>\n\n<em>{str(error)}</em>",
                    parse_mode=teleapi.ParseMode.HTML
                )
            ],
        )

        if update.message:
            view = UnknownErrorMessageView(error_id, error, update)

            await update.message.reply(
                text=get_unknown_error_message_text(),
                view=view,
                parse_mode=teleapi.ParseMode.HTML
            )
