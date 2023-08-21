import teleapi


class MainExecutor(teleapi.Executor):
    @teleapi.Executor.executor_command(name='test')
    async def test_command(self, message: teleapi.Message, **_) -> None:
        await message.reply("Hello world")
