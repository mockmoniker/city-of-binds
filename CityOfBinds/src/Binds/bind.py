from CityOfBinds.src.Triggers.trigger import Trigger, WASDTrigger
from CityOfBinds.src.Triggers.mixin import TriggerMixin
from CityOfBinds.src.SlashCommands.commandgroup import CommandGroup
from CityOfBinds.src.SlashCommands.mixin import CommandGroupMixin

class BindConstants:
    MAX_BIND_LENGTH = 255 # TODO: verify if 255 is command max or full bind max (2025/11/27) 
    
class Bind(TriggerMixin, CommandGroupMixin): # TODO: deprecate CommandGroupMixin? Bind should maybe just be a commandGroup with trigger (2025/11/29) 
    def __init__(
        self,
        trigger: Trigger | str,
        commands: CommandGroup | list[str] = None
    ):
        super().__init__()
        """Initialize the bind with a trigger and slash command list."""
        self.trigger = trigger
        self.commands = commands if commands is not None else CommandGroup()

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

    # region Override Methods
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        movement_command = CommandGroup().add_movement(self._get_direction(self.trigger))
        commands_with_movement = movement_command + self.commands
        return self._build_bind_string_from_components(self.trigger, commands_with_movement)
    
    # endregion

    # region Helper Methods
    def _get_direction(self, trigger: Trigger) -> str:
        return WASDTrigger.KEY_TO_DIRECTION_MAP[trigger.key]

    # endregion

class iWASDBind(WASDBind):
    # region Override Methods
    def _get_direction(self, trigger: Trigger) -> set:
        direction = super()._get_direction(trigger)
        opposite_directions = {
            "forward": "backward",
            "backward": "forward",
            "left": "right",
            "right": "left"
        }
        return opposite_directions[direction]
    
    # endregion
    