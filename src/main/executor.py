import teleapi
from .search import search_manager, Track


class MainExecutor(teleapi.Executor):
    @teleapi.Command.command_parameter(name='url')
    @teleapi.Executor.executor_command(name='find')
    async def test_command(self, message: teleapi.Message, parameters, **_) -> None:
        url = parameters['url']

        found = await search_manager.search(query=url)

        print(found.result)

        if isinstance(found.result, Track):
            track = found.result
            data_source = await track.get_data_source()
            print(data_source)

            await message.reply(
                text=f"""<b>Вот, что я нашел по запросу {url}:</b>\n{track.title}\nВот ссылка на скачивание аудио:{data_source.audio_source[0]}""",
                parse_mode=teleapi.ParseMode.HTML,
                disable_web_page_preview=True
            )
