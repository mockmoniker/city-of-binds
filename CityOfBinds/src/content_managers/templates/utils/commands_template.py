from .command_factory import _CommandFactory
from ....game.utils import _Power
from ....game.utils import _CommandGroup, CommandGroupConstants
from .....utils import ListTemplate, Pool


class _CommandsTemplate(_CommandGroup, ListTemplate):
    def __init__(self):
        _CommandGroup.__init__(self)
        ListTemplate.__init__(self, self._commands)

    def add_power_pool(self, powers: list[str]) -> "_CommandsTemplate":
        return self.add_command_arguments_pool(
            CommandGroupConstants.POWEXEC_NAME, [_Power(power) for power in powers]
        )

    def add_toggle_on_power_pool(self, powers: list[str]) -> "_CommandsTemplate":
        return self.add_command_arguments_pool(
            CommandGroupConstants.POWEXEC_TOGGLE_ON, [_Power(power) for power in powers]
        )

    def add_command_arguments_pool(
        self, command: str, *arg_lists: list
    ) -> "_CommandsTemplate":
        if not arg_lists:
            return self  # TODO: error or just append command? (2025/11/28)

        command_factory = _CommandFactory(command, *arg_lists)
        command_pool = Pool(f"{command}_{id(arg_lists)}", command_factory.build_all())

        self._commands.append(command_pool)
        return self

    def _build_one(self) -> _CommandGroup:
        return _CommandGroup(super()._build_one())
