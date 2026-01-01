from ...configs.constants import MacroCommands
from ..utils.commands.commands_mixin import _CommandsMixin


class Macro(_CommandsMixin):
    MACRO_COMMAND = MacroCommands.MACRO

    def __init__(self, name: str, commands: list[str] = None):
        """
        Initialize a new Macro with a name and optional commands.

        Args:
            name: Name of the macro
            commands: List of slash command strings to include in the macro
        """
        _CommandsMixin.__init__(self, commands)
        self.name = name

    def macro_string(self) -> str:
        return self._build_macro_string()

    def _build_macro_string(self) -> str:
        return self._build_macro_string_from_components(self.name, self.commands)

    def _build_macro_string_from_components(self, *args) -> str:
        """Build macro string"""
        # TODO: handle checking if args need quotations (2025/12/30)
        return f"{self.MACRO_COMMAND} {" ".join(str(arg) for arg in args)}"

    def __str__(self):
        return self.macro_string()
