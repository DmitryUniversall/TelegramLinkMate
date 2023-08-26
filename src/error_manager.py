import os.path

import teleapi
from .exceptions.exceptions import UserError
from .utils.text import strip_lines
from teleapi.generics.http.methods.messages.send import send_media_group
import pickle


def get_error_message_text(text: str) -> str:
    return strip_lines(
        f"""
        ❌ <b>Произошла ошибка:</b>
        └<em>{text}</em>
        """
    )


class UnknownErrorMessageView(teleapi.View):
    def __init__(self, error: Exception, update: teleapi.Update) -> None:
        super().__init__()

        self.error = error
        self.update = update

    @teleapi.View.view_button(text="📢 Сообщить об ошибке", row=0)
    async def report_button(self, callback_query: teleapi.CallbackQuery, **_) -> None:
        await send_media_group(
            chat_id=teleapi.project_settings.OWNER_CHAT_ID,
            media=[
                teleapi.InputMediaDocument(
                    data=pickle.dumps(self.error),
                    filename="error_object.pkl"
                ),
                teleapi.InputMediaDocument(
                    data=pickle.dumps(self.update),
                    filename="update_object.pkl"
                ),
                teleapi.InputMediaDocument(
                    media=os.path.join(teleapi.project_settings.PROCESS_LOG_DIR, "debug.log"),
                    filename="recent_logs.log",
                    caption=f"<b>Unknown error occurred:</b>\n<em>{str(self.error)}</em>",
                    parse_mode=teleapi.ParseMode.HTML
                )
            ],
        )

        await callback_query.answer("Спасибо за сообщение об ошибке. Мы постараемся её исправить")


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

        if update.message:
            view = UnknownErrorMessageView(error, update)
            await update.message.reply(
                text=get_error_message_text("Неизвестная ошибка"),
                view=view,
                parse_mode=teleapi.ParseMode.HTML
            )
