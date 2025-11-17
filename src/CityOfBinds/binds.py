from functools import cached_property
from CityOfBinds.trigger import Trigger, WASDTrigger
from CityOfBinds.commandgroup import CommandGroup

class BindConstants:
    MAX_BIND_LENGTH = 255

class Bind:
    TRIGGER_TYPE = Trigger

    # Initialization
    def __init__(self, trigger_string: str, commands_string_list: list[str] = None):
        """Initialize the bind with a trigger and slash command list."""
        self._trigger = None
        self._commands = None

        self.trigger = trigger_string
        self.commands = commands_string_list if commands_string_list is not None else []

    # region Bind Properties
    @property
    def trigger(self) -> Trigger:
        return self._trigger
    
    @trigger.setter
    def trigger(self, trigger_string: str):
        self._trigger = self.TRIGGER_TYPE(trigger_string)
    
    @property
    def commands(self) -> CommandGroup:
        return self._commands
    
    @commands.setter
    def commands(self, commands_string_list: list[str]):
        self._commands = CommandGroup(commands_string_list)

    @cached_property
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

    def is_empty(self) -> bool:
        """Helper function to ensure the bind is not empty."""
        return len(self.commands) == 0

    def is_over_bind_length(self) -> bool:
        """Helper function to ensure the total bind string does not exceed max character length."""
        return self.bind_length > BindConstants.MAX_BIND_LENGTH

    # endregion

    # region Helper Methods
    def _build_bind_string(self) -> str:
        """Helper function to build the bind string."""
        return self._build_bind_string_from_components(trigger=self.trigger, commands=self.commands)

    def _build_bind_string_from_components(self, trigger: Trigger, commands: CommandGroup) -> str:
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
            raise ValueError(f"Bind exceeds maximum length of {BindConstants.MAX_BIND_LENGTH} characters. Current length is '{self.bind_length}'.")

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

class WASDBind(Bind):
    TRIGGER_TYPE = WASDTrigger

    # region Helper Methods
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        movement_command = CommandGroup()
        movement_command.prepend_movement(WASDTrigger.KEY_TO_DIRECTION_MAP[self.trigger.key])
        commands_with_movement = movement_command + self.commands
        return self._build_bind_string_from_components(trigger=self.trigger, commands=commands_with_movement)
    
    # endregion
