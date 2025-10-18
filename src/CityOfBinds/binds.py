from functools import cached_property
from CityOfBinds.trigger import Trigger, WASDTrigger
from CityOfBinds.slashcommand import SlashCommand
from CityOfBinds.power import Power

class BindConstants:
    MAX_BIND_LENGTH = 255
    COMMAND_DELIM = "$$"
    
    # Power execution types
    POWEXEC_TOGGLE_OFF = "powexectoggleoff"
    POWEXEC_TOGGLE_ON = "powexectoggleon"
    POWEXEC_AUTO = "powexecauto"
    
    # Movement commands
    KEY_TO_DIRECTION_MAP = {
        "W": "+forward",
        "A": "+left",
        "S": "+backward",
        "D": "+right",
        "SPACE": "+up"
    }

class Bind:
    TRIGGER_TYPE = Trigger

    ### Initialization
    def __init__(self, trigger_string: str, slash_commands_string_list: list[str] = None):
        """Initialize the bind with a trigger and slash command list."""

        self._trigger = None
        self._slash_commands = None

        self.trigger = trigger_string
        self.slash_commands = slash_commands_string_list if slash_commands_string_list is not None else []

    ### Properties
    @property
    def trigger(self) -> Trigger:
        return self._trigger
    
    @trigger.setter
    def trigger(self, trigger_string: str):
        self._trigger = self.TRIGGER_TYPE(trigger_string)

    @property
    def slash_commands(self) -> list[SlashCommand]:
        return self._slash_commands.copy()
    
    @slash_commands.setter
    def slash_commands(self, slash_commands_string_list: list[str]):
        self._slash_commands = self._convert_strings_to_objects(slash_commands_string_list, SlashCommand)
    
    @cached_property
    def bind_string(self) -> str:
        return self._build_bind_string()
    
    @property
    def bind_length(self) -> int:
        return len(self.bind_string)

    ### Methods
    def validate(self):
        self._throw_error_on_empty_bind()
        self._throw_error_on_bind_too_long()

    def is_empty(self) -> bool:
        """Helper function to ensure the bind is not empty."""
        return len(self._slash_commands) == 0

    def is_over_bind_length(self) -> bool:
        """Helper function to ensure the total bind string does not exceed max character length."""
        return self.bind_length > BindConstants.MAX_BIND_LENGTH

    ### Helpers
    def _build_bind_string(self) -> str:
        """Helper function to build the bind string."""
        return self._build_bind_string_from_components(trigger=self.trigger, slash_commands=self.slash_commands)

    def _build_bind_string_from_components(self, trigger: Trigger, slash_commands: list[SlashCommand]) -> str:
        """Helper function to build the bind string from its components."""
        return f"{trigger} \"{BindConstants.COMMAND_DELIM.join(slash_command.slash_command_string for slash_command in slash_commands)}\""

    def _convert_strings_to_objects(self, string_list: list[str], object_type):
        """Helper function to convert a list of strings to a list of objects of the specified type."""
        return [object_type(string) for string in string_list]

    ### Error Checking/Validation
    def _throw_error_on_empty_bind(self):
        """Helper function to ensure the slash commands list is not empty."""
        if self.is_empty():
            raise ValueError("Bind must contain one or more slash commands.")
        
    def _throw_error_on_bind_too_long(self):
        """Helper function to ensure the bind does not exceed max length."""
        if self.is_over_bind_length():
            raise ValueError(f"Bind exceeds maximum length of {BindConstants.MAX_BIND_LENGTH} characters. Current length is '{self.bind_length}'.")

    ### Overrides
    def __repr__(self) -> str:
        """Override the default representation."""
        return f"Bind(trigger={self.trigger}, slash_commands={self.slash_commands})"
    
    def __str__(self) -> str:
        """Override the default string representation."""
        return self.bind_string

    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, Bind):
            return False
        return self.bind_string == other.bind_string

class ToggleBind(Bind):

    def __init__(self, 
                 trigger_string: str, 
                 slash_commands_string_list: list[str] = None, 
                 toggle_off_powers_string_list: list[str] = None, 
                 toggle_on_powers_string_list: list[str] = None, 
                 auto_power_string: str = ""):
        self._toggle_off_powers = None
        self._toggle_on_powers = None
        self._auto_power = None

        super().__init__(trigger_string=trigger_string, slash_commands_string_list=slash_commands_string_list)

        self.toggle_off_powers = toggle_off_powers_string_list if toggle_off_powers_string_list is not None else []
        self.toggle_on_powers = toggle_on_powers_string_list if toggle_on_powers_string_list is not None else []
        self.auto_power = auto_power_string

    ### Properties
    @property
    def toggle_off_powers(self) -> list[Power]:
        return self._toggle_off_powers.copy()
    
    @toggle_off_powers.setter
    def toggle_off_powers(self, toggle_off_powers_string_list: list[str]):
        self._toggle_off_powers = self._convert_strings_to_objects(toggle_off_powers_string_list, Power)

    @property
    def toggle_on_powers(self) -> list[Power]:
        return self._toggle_on_powers.copy()
    
    @toggle_on_powers.setter
    def toggle_on_powers(self, toggle_on_powers_string_list: list[str]):
        self._toggle_on_powers = self._convert_strings_to_objects(toggle_on_powers_string_list, Power)

    @property
    def auto_power(self) -> Power:
        return self._auto_power

    @auto_power.setter
    def auto_power(self, auto_power_string: str):
        if auto_power_string:
            self._auto_power = Power(auto_power_string)
        else:
            self._auto_power = None

    ### Methods
    def is_empty(self) -> bool:
        return super().is_empty() and not self.toggle_off_powers and not self.toggle_on_powers and not self.auto_power

    ### Helpers
    def _get_powexec_slash_command_from_power(self, powexec_type: str, power: Power) -> SlashCommand:
        """Helper function to convert a single power to a powexec command."""
        if power:
            return SlashCommand(f"{powexec_type} {power}")
        return None

    def _get_powexec_slash_command_list_from_power_list(self, powexec_type: str, power_list: list[Power]) -> list[SlashCommand]:
        """Helper function to convert a list of powers to powexec commands."""
        return [self._get_powexec_slash_command_from_power(powexec_type, power) for power in power_list]

    def _get_toggle_off_slash_command_list_from_power_list(self, power_list: list[Power]) -> list[SlashCommand]:
        """Helper function to convert a list of powers to powexectoggleoff commands."""
        return self._get_powexec_slash_command_list_from_power_list(BindConstants.POWEXEC_TOGGLE_OFF, power_list)

    def _get_toggle_on_slash_command_list_from_power_list(self, power_list: list[Power]) -> list[SlashCommand]:
        """Helper function to convert a list of powers to powexectoggleon commands."""
        return self._get_powexec_slash_command_list_from_power_list(BindConstants.POWEXEC_TOGGLE_ON, power_list)

    def _build_bind_string(self) -> str:
        """Helper function to build the toggle bind string."""
        toggle_off_slash_command_list = self._get_toggle_off_slash_command_list_from_power_list(self.toggle_off_powers)
        toggle_on_slash_command_list = self._get_toggle_on_slash_command_list_from_power_list(self.toggle_on_powers)
        auto_power_slash_command_list = [self._get_powexec_slash_command_from_power(BindConstants.POWEXEC_AUTO, self.auto_power)] if self.auto_power else []

        combined_slash_commands = toggle_off_slash_command_list + toggle_on_slash_command_list + auto_power_slash_command_list + self.slash_commands

        return self._build_bind_string_from_components(self.trigger, combined_slash_commands)
    
class WASDBind(ToggleBind):
    TRIGGER_TYPE = WASDTrigger

    ### Initialization
    def __init__(self, 
                 trigger_string: str, 
                 slash_commands_string_list: list[str] = None,
                 toggle_off_powers_string_list: list[str] = None,
                 movement_powers_string_list: list[str] = None, 
                 toggle_on_powers_string_list: list[str] = None, 
                 auto_power_string: str = None):
        """Initialize the WASD bind with a trigger and a default movement slash command."""
        self._movement_powers = None

        super().__init__(trigger_string=trigger_string,
                         slash_commands_string_list=slash_commands_string_list,
                         toggle_off_powers_string_list=toggle_off_powers_string_list,
                         toggle_on_powers_string_list=toggle_on_powers_string_list,
                         auto_power_string=auto_power_string)

        self.movement_powers = movement_powers_string_list if movement_powers_string_list is not None else []

    ### Properties
    @property
    def movement_powers(self) -> list[Power]:
        return self._movement_powers.copy()
    
    @movement_powers.setter
    def movement_powers(self, movement_powers_string_list: list[str]):
        self._movement_powers = self._convert_strings_to_objects(movement_powers_string_list, Power)

    ### Methods
    def is_empty(self) -> bool:
        return super().is_empty() and not self.movement_powers
    
    ### Helpers
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        movement_slash_command = self._get_movement_slash_command_from_trigger(self.trigger)
        toggle_off_slash_commands = self._get_toggle_off_slash_command_list_from_power_list(self.toggle_off_powers)
        movement_slash_commands = self._get_toggle_on_slash_command_list_from_power_list(self.movement_powers)
        toggle_on_slash_commands = self._get_toggle_on_slash_command_list_from_power_list(self.toggle_on_powers)
        auto_power_slash_command_as_list = [self._get_powexec_slash_command_from_power(BindConstants.POWEXEC_AUTO, self.auto_power)] if self.auto_power else []

        combined_slash_commands = [movement_slash_command] + toggle_off_slash_commands + movement_slash_commands + toggle_on_slash_commands + auto_power_slash_command_as_list + self.slash_commands

        return self._build_bind_string_from_components(self.trigger, combined_slash_commands)
    
    def _get_movement_slash_command_from_trigger(self, trigger: Trigger) -> SlashCommand:
        """Helper function to get the WASD direction for the trigger."""
        return SlashCommand(BindConstants.KEY_TO_DIRECTION_MAP[trigger.key])