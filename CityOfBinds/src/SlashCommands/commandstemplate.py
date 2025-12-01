from CityOfBinds.src.SlashCommands.power import Power
from CityOfBinds.src.SlashCommands.commandgroup import (
    CommandGroup,
    CommandGroupConstants,
)
from CityOfBinds.src.SlashCommands.commandfactory import CommandFactory
from CityOfBinds.utils.Templates.pool import Pool
from CityOfBinds.utils.Templates.templates import ListTemplate


class CommandsTemplate(CommandGroup, ListTemplate):
    def __init__(self):
        CommandGroup.__init__(self)
        ListTemplate.__init__(self, self._commands)

    def add_power_pool(self, powers: list[str]) -> "CommandsTemplate":
        return self.add_command_arguments_pool(
            CommandGroupConstants.POWEXEC_NAME, [Power(power) for power in powers]
        )

    def add_toggle_on_power_pool(self, powers: list[str]) -> "CommandsTemplate":
        return self.add_command_arguments_pool(
            CommandGroupConstants.POWEXEC_TOGGLE_ON, [Power(power) for power in powers]
        )

    def add_command_arguments_pool(
        self, command: str, *arg_lists: list
    ) -> "CommandsTemplate":
        if not arg_lists:
            return self  # TODO: error or just append command? (2025/11/28)

        command_factory = CommandFactory(command, *arg_lists)
        command_pool = Pool(f"{command}_{id(arg_lists)}", command_factory.build_all())

        self._commands.append(command_pool)
        return self

    def _build_one(self) -> CommandGroup:
        return CommandGroup(super()._build_one())
