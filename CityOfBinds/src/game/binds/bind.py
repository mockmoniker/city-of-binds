from ...configs.constants import GameConstants
from ..utils.commands.command_group import _CommandGroup
from ..utils.commands.commands_mixin import _CommandsMixin
from ..utils.triggers.trigger import _Trigger
from ..utils.triggers.trigger_mixin import _TriggerMixin


class Bind(_TriggerMixin, _CommandsMixin):
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
    def bind_string(self) -> str:
        """Get the complete bind string ready for use in bind files.

        Returns:
            Formatted bind string in the format: 'TRIGGER "command1$$command2"'
        """
        return self._build_bind_string()

    @property
    def bind_length(self) -> int:
        """Get the character length of the bind string.

        Returns:
            Number of characters in the complete bind string
        """
        return len(self.bind_string)

    # endregion

    # region Bind Methods
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
    def _build_bind_string(self) -> str:
        """
        Build the complete bind string from trigger and commands.

        Handles special cases like key-up triggers by adding "+" prefix when needed.

        Returns:
            Complete bind string ready for bind file output
        """
        commands = self.commands
        # Add "+" prefix for key-up triggers if first command doesn't have a prefix
        if self.trigger_on_key_up and not commands[0].prefix:
            modifier_command = _CommandGroup(GameConstants.ENABLE_KEY_UP_PREFIX)
            commands = modifier_command + commands
        return self._build_bind_string_from_components(
            trigger=self.trigger, commands=commands
        )

    def _build_bind_string_from_components(
        self, trigger: _Trigger, commands: _CommandGroup
    ) -> str:
        """
        Combine trigger and commands into a properly formatted bind string.

        Args:
            trigger: The trigger object containing key/modifier information
            commands: The command group containing all commands to execute

        Returns:
            Formatted string in the format: 'TRIGGER "commands"'
        """
        return f"{str(trigger)} {str(commands)}"

    # endregion

    # region Error Checking Methods
    def _throw_error_if_empty_bind(self):
        """
        Raise ValueError if the bind has no commands.

        Raises:
            ValueError: If bind is empty (no commands)
        """
        if self.is_empty():
            raise ValueError("Bind must contain one or more commands.")

    def _throw_error_if_bind_too_long(self):
        """
        Raise ValueError if the bind exceeds maximum character length.

        Raises:
            ValueError: If bind string is longer than MAX_BIND_LENGTH
        """
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

    def __str__(self) -> str:
        """
        Return the bind string representation for use in bind files.

        Returns:
            Complete bind string ready for bind file output
        """
        return self.bind_string

    def __eq__(self, other):
        """
        Compare two Bind objects for equality based on their bind strings.

        Args:
            other: Another object to compare against

        Returns:
            True if both objects are Binds with identical bind strings
        """
        if not isinstance(other, Bind):
            return False
        return self.bind_string == other.bind_string

    # endregion
