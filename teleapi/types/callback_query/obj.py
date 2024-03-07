from .model import CallbackQueryModel
from teleapi.core.http.request import method_request
from teleapi.core.utils.collections import clear_none_values
from teleapi.core.http.request.api_method import APIMethod


class CallbackQuery(CallbackQueryModel):
    def __eq__(self, other) -> bool:
        return isinstance(other, CallbackQuery) and other.id == self.id

    async def answer(self, text: str = None, show_alert: bool = False, url: str = None, cache_time: int = None) -> bool:
        request_data = clear_none_values({
            "callback_query_id": self.id,
            "text": text,
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time
        })

        response, data = await method_request("POST", APIMethod.ANSWER_CALLBACK_QUERY, data=request_data)

        self.is_answered = True

        return bool(data)
