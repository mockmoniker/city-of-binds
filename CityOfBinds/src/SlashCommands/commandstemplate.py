from CityOfBinds.src.SlashCommands.power import Power
from CityOfBinds.src.SlashCommands.slashcommand import SlashCommand
from CityOfBinds.src.SlashCommands.commandgroup import CommandGroup, CommandGroupConstants
from CityOfBinds.src.SlashCommands.commandfactory import CommandFactory
from CityOfBinds.utils.Templates.pool import Pool
from CityOfBinds.utils.Templates.templates import ListTemplate, StringTemplate

class CommandsTemplate(CommandGroup, ListTemplate):
    def __init__(self):
        CommandGroup.__init__(self)
        ListTemplate.__init__(self, self._commands)

    def add_power_pool(self, powers: list[ str | Power]) -> 'CommandsTemplate':
        return self.add_command_arguments_pool(CommandGroupConstants.POWEXEC_NAME, [str(power) for power in powers])
    
    def add_toggle_on_power_pool(self, powers: list[ str | Power]) -> 'CommandsTemplate':
        return self.add_command_arguments_pool(CommandGroupConstants.POWEXEC_TOGGLE_ON, [str(power) for power in powers])

    def add_command_arguments_pool(self, command: str, *arg_lists: list[str]) -> 'CommandsTemplate':
        if not arg_lists:
            return self # TODO: error or just append command? (2025/11/28) 
        
        lengths = [len(arg_list) for arg_list in arg_lists]
        all_lengths_equal = len(set(lengths)) == 1

        build_count = 1
        if all_lengths_equal:
            build_count = lengths[0]
        else:
            for arg_list in arg_lists:
                build_count *= len(arg_list)

        command_factory = CommandFactory(command, *arg_lists)
        command_pool = Pool(f"{command}_{id(arg_lists)}", command_factory.build(build_count))

        self._commands.append(command_pool)
        return self

    def _build_one(self) -> CommandGroup:
        return CommandGroup(super()._build_one())