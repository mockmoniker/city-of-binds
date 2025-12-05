import copy
from .command_group import _CommandGroup


class _CommandsMixin:
    def __init__(self, commands: list[str] = None):
        self._commands = None
        self.commands = commands or []

    @property
    def commands(self) -> _CommandGroup:
        return self._commands

    @commands.setter
    def commands(self, value):
        if isinstance(value, list):
            self._commands = _CommandGroup(value)
        elif isinstance(value, _CommandGroup):
            self._commands = copy.deepcopy(value)
        else:
            self._throw_set_commands_type_error(value)

    def _throw_set_commands_type_error(self, value):
        raise TypeError(
            f"Invalid type '{type(value)}'. Commands must be set using a list of strings or a CommandGroup instance."
        )
