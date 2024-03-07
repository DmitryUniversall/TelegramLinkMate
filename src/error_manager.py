import os
import pickle
import random
import teleapi

from src.main.exceptions import ErrorMessageException
from src.main.ui.error import ErrorMessageView
from src.core.utils.errors import get_traceback_text
import logging

_logger = logging.getLogger(__name__)


class BotErrorManager(teleapi.ErrorManager):
    @teleapi.ErrorManager.manager_handler(exception_cls=ErrorMessageException)
    async def user_error_handler(self, error: ErrorMessageException, update: teleapi.Update, **_) -> bool:
        if update.message is None:
            return False

        view = ErrorMessageView(str(error))
        await view.send(chat=update.message.chat)

        return True

    async def handle_unknown_error(self, error: Exception, update: teleapi.Update) -> None:
        await super().handle_unknown_error(error, update)

        if update.message:
            message = update.message
        elif update.callback_query:
            message = update.callback_query.message
        else:
            return

        view = ErrorMessageView(None)
        await view.send(chat=message.chat)

        if teleapi.project_settings.DEBUG:
            _logger.error(f"Unknown error on update {update.id}: {get_traceback_text(error)}")
            return

        error_id = random.randint(1000, 1000000)
        await message.chat.send_media_group(
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
                    media=os.path.join(teleapi.project_settings.CURRENT_PROCESS_LOGS_DIR, "debug.log"),
                    filename="recent_logs.log",
                    caption=f"<b>Unknown error ({error_id}) occurred:</b>\n\n<em>{str(error)}</em>",
                    parse_mode=teleapi.ParseMode.HTML
                )
            ],
        )
