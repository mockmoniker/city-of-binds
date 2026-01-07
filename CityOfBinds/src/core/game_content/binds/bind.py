from ...._configs.constants import GameConstants
from ..command_group.command_group import CommandGroup
from ..command_group.commands_mixin import _CommandsMixin
from ..utils.game_strings import _BindString
from ..utils.triggers.trigger import _Trigger
from ..utils.triggers.trigger_mixin import _TriggerMixin


class Bind(_TriggerMixin, _CommandsMixin, _BindString):
    """
    Represents a game bind that maps a trigger (key + optional modifier) to one or more commands.

    A Bind combines a trigger (like "F1" or "SHIFT+F1") with a list of slash commands
    to create a bind string that can be used in game bind files.

    Example:
        >>> bind = Bind("F1", ["powexecname heal other", "say healing!"])
        >>> str(bind)  # 'F1 "powexecname heal other$$say healing!"'

    Attributes:
        trigger_on_key_up: When true, allows the bind to trigger on key release in addition to key press.
    """

    def __init__(self, trigger: str, commands: list[str] = None):
        """
        Initialize a new Bind with a trigger and optional commands.

        Args:
            trigger: Key and optional modifier string (e.g., "F1", "SHIFT+F1", "Q")
            commands: List of slash command strings to execute when triggered
        """
        _TriggerMixin.__init__(self, trigger)
        _CommandsMixin.__init__(self, commands)
        self.trigger_on_key_up = False

    # region Bind Properties
    @property
    def bind_length(self) -> int:
        """Get the character length of the bind string.

        Returns:
            Number of characters in the complete bind string
        """
        return len(self.get_str())

    # endregion

    # region Bind Methods
    def get_str(self) -> str:
        """Get the complete bind string."""
        return self._build_bind_string()

    def _build_bind_string(self) -> str:
        """Build complete bind string, handling key-up triggers."""
        commands = self.commands
        if self.trigger_on_key_up and not commands[0].prefix:
            commands = self._add_key_up_prefix(commands)
        return self._build_bind_string_from_components(
            trigger=self.trigger, commands=commands
        )

    def validate(self):
        """
        Validate the bind for common issues.

        Raises:
            ValueError: If bind is empty or exceeds maximum length
        """
        self._throw_error_if_empty_bind()
        self._throw_error_if_bind_too_long()

    def is_valid(self) -> bool:
        """
        Check if the bind is valid without raising exceptions.

        Returns:
            True if bind has commands and is within length limits
        """
        return not self.is_empty() and not self.is_over_bind_length()

    def is_empty(self) -> bool:
        """
        Check if the bind has no commands.

        Returns:
            True if the bind has no commands, False otherwise
        """
        return len(self.commands) == 0

    def is_over_bind_length(self) -> bool:
        """
        Check if the bind string exceeds the maximum allowed length.

        Returns:
            True if bind string is too long, False otherwise
        """
        return self.bind_length > GameConstants.MAX_BIND_LENGTH

    # endregion

    # region Helper Methods
    def _add_key_up_prefix(self, commands: CommandGroup) -> CommandGroup:
        """Adds a '+' to beginning of commands list to enable key-up triggering."""
        prefix_only_command = CommandGroup(GameConstants.ENABLE_KEY_UP_PREFIX)
        commands = prefix_only_command + commands
        return commands

    def _build_bind_string_from_components(
        self, trigger: _Trigger, commands: CommandGroup
    ) -> str:
        """Combine trigger and commands into formatted bind string."""
        return f"{str(trigger)} {str(commands)}"

    # endregion

    # region Error Checking Methods
    def _throw_error_if_empty_bind(self):
        """Raise ValueError if bind has no commands."""
        if self.is_empty():
            raise ValueError("Bind must contain one or more commands.")

    def _throw_error_if_bind_too_long(self):
        """Raise ValueError if bind exceeds maximum length."""
        if self.is_over_bind_length():
            raise ValueError(
                f"Bind exceeds maximum length of {GameConstants.MAX_BIND_LENGTH} characters. Current length is '{self.bind_length}'."
            )

    # endregion

    # region Dunder Methods
    def __repr__(self) -> str:
        """
        Return a detailed string representation for debugging.

        Returns:
            String showing class name, trigger, and commands
        """
        return f"{self.__class__.__name__}(trigger={self.trigger}, commands={self.commands})"

    # endregion
