from typing import Type, List

import teleapi


class HelpCommandView(teleapi.View):
    def __init__(self, commands: List[Type[teleapi.Command]], commands_in_row: int = 1) -> None:
        super().__init__()

        self.commands_matrix = [commands[index: index + commands_in_row] for index in range(0, len(commands), commands_in_row)]

        for row_index, row in enumerate(self.commands_matrix):
            for command_index, command in enumerate(row):
                if hasattr(command.Meta, 'description'):
                    button = teleapi.button(
                            text=getattr(command, 'name'),
                            row=row_index,
                            place=command_index,
                            command=command
                    )(self.on_command_button_click)

                    self.register_button(
                        button(self)
                    )

    @staticmethod
    async def on_command_button_click(button: teleapi.InlineViewButton, callback_query: teleapi.CallbackQuery, **_) -> None:
        command = getattr(button.Meta, 'command')

        if hasattr(command.Meta, 'photo'):
            await callback_query.message.chat.send_photo(
                photo=getattr(command.Meta, 'photo'),
                caption=getattr(command.Meta, 'description'),
                parse_mode=teleapi.ParseMode.HTML
            )
        else:
            await callback_query.message.chat.send_message(
                text=getattr(command.Meta, 'description'),
                parse_mode=teleapi.ParseMode.HTML
            )


class HelpCommand(teleapi.Command):
    class Meta:
        name = 'help'

    async def execute(self, message: teleapi.Message, **kwargs) -> None:
        view = HelpCommandView(getattr(self.executor, '_commands'))

        await message.reply(
            text="<b>Добро пожаловать в справочный раздел!</b>\n"
                 "<b>Вот список доступных команд:</b>",
            parse_mode=teleapi.ParseMode.HTML,
            view=view
        )
