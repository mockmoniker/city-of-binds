from CityOfBinds.src.SlashCommands.power import Power
from CityOfBinds.src.SlashCommands.commandgroup import CommandGroup, CommandGroupConstants
from CityOfBinds.src.SlashCommands.commandfactory import CommandFactory
from CityOfBinds.utils.Templates.pool import Pool
from CityOfBinds.utils.Templates.templates import ListTemplate

class CommandsTemplate(CommandGroup, ListTemplate):
    def __init__(self):
        CommandGroup.__init__(self)
        ListTemplate.__init__(self, self._commands)

    def add_power_pool(self, powers: list[str]) -> 'CommandsTemplate':
        return self.add_command_arguments_pool(CommandGroupConstants.POWEXEC_NAME, [Power(power) for power in powers])
    
    def add_toggle_on_power_pool(self, powers: list[str]) -> 'CommandsTemplate':
        return self.add_command_arguments_pool(CommandGroupConstants.POWEXEC_TOGGLE_ON, [Power(power) for power in powers])

    def add_command_arguments_pool(self, command: str, *arg_lists: list) -> 'CommandsTemplate':
        if not arg_lists:
            return self # TODO: error or just append command? (2025/11/28) 
        
        build_count = self._get_unique_build_count(*arg_lists)

        command_factory = CommandFactory(command, *arg_lists)
        command_pool = Pool(f"{command}_{id(arg_lists)}", command_factory.build(build_count))

        self._commands.append(command_pool)
        return self

    def _get_unique_build_count(self, *lists: list) -> int:
        build = 1
        unique_lengths = set([len(arg_list) for arg_list in lists])
        for unique_length in unique_lengths:
            build *= unique_length
        return build

    def _build_one(self) -> CommandGroup:
        return CommandGroup(super()._build_one())