from ..utils import _Trigger, _TriggerMixin
from ..utils import _CommandsMixin, _CommandGroup
from ...configs.constants import GameConstants


class Bind(_TriggerMixin, _CommandsMixin):
    def __init__(self, trigger: str, commands: list[str] = None):
        _TriggerMixin.__init__(self, trigger)
        _CommandsMixin.__init__(self, commands)
        self.trigger_on_key_up = False

    # region Bind Properties
    @property
    def bind_string(self) -> str:
        return self._build_bind_string()

    @property
    def bind_length(self) -> int:
        return len(self.bind_string)

    # endregion

    # region Bind Methods
    def validate(self):
        self._throw_error_if_empty_bind()
        self._throw_error_if_bind_too_long()

    def is_valid(self) -> bool:
        return not self.is_empty() and not self.is_over_bind_length()

    def is_empty(self) -> bool:
        """Helper function to ensure the bind is not empty."""
        return len(self.commands) == 0

    def is_over_bind_length(self) -> bool:
        """Helper function to ensure the total bind string does not exceed max character length."""
        return self.bind_length > GameConstants.MAX_BIND_LENGTH

    # endregion

    # region Helper Methods
    def _build_bind_string(self) -> str:
        commands = self.commands
        if self.trigger_on_key_up and not commands[0].prefix:
            modifier_command = _CommandGroup("+")
            commands = modifier_command + commands
        return self._build_bind_string_from_components(
            trigger=self.trigger, commands=commands
        )

    def _build_bind_string_from_components(
        self, trigger: _Trigger, commands: _CommandGroup
    ) -> str:
        """Helper function to build the bind string from its components."""
        return f"{str(trigger)} {str(commands)}"

    # endregion

    # region Error Checking Methods
    def _throw_error_if_empty_bind(self):
        """Helper function to ensure the commands list is not empty."""
        if self.is_empty():
            raise ValueError("Bind must contain one or more commands.")

    def _throw_error_if_bind_too_long(self):
        """Helper function to ensure the bind does not exceed max length."""
        if self.is_over_bind_length():
            raise ValueError(
                f"Bind exceeds maximum length of {GameConstants.MAX_BIND_LENGTH} characters. Current length is '{self.bind_length}'."
            )

    # endregion

    # region Dunder Methods
    def __repr__(self) -> str:
        """Override the default representation."""
        return f"{self.__class__.__name__}(trigger={self.trigger}, commands={self.commands})"

    def __str__(self) -> str:
        """Override the default string representation."""
        return self.bind_string

    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, Bind):
            return False
        return self.bind_string == other.bind_string

    # endregion
