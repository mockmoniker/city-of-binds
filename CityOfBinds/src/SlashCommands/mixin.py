import copy
from CityOfBinds.src.SlashCommands.commandgroup import CommandGroup


class CommandGroupMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._commands = None  # TODO: initialize public member here? (2025/11/28)

    @property
    def commands(self) -> CommandGroup:
        return self._commands

    @commands.setter
    def commands(self, value):
        if isinstance(value, list):
            self._commands = CommandGroup(value)
        elif isinstance(value, CommandGroup):
            self._commands = copy.deepcopy(value)
        else:
            self._throw_set_commands_type_error(value)

    def _throw_set_commands_type_error(self, value):
        raise TypeError(
            f"Invalid type '{type(value)}'. Commands must be set using a CommandGroup instance or a list of command strings."
        )
