import teleapi
import asyncio


async def send_chat_action(chat: teleapi.Chat, action: teleapi.ChatAction, interval: int = 5):
    while True:
        await chat.send_action(action)
        await asyncio.sleep(interval)


async def get_query_dialog(executor: teleapi.BaseExecutor, chat: teleapi.Chat) -> str:
    while True:
        await chat.send_message(
            text="Укажите примерное название или ссылку видео/трек/плейлист/альбом"
        )

        _, data = await executor.wait_for(
            event_type=teleapi.UpdateEvent.ON_MESSAGE,
            filter_=lambda _, x: x['message'].chat == chat
        )

        msg = data['message']

        if msg.text:
            return msg.text
