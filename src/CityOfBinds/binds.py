from copy import deepcopy
from CityOfBinds.slashcommands import SlashCommands
from CityOfBinds.trigger import Trigger

class Bind:
    MAX_BIND_LENGTH = 255

    ### Initialization
    def __init__(self, trigger: str, slash_commands: list[str]):
        """Initialize the bind with a trigger and slash command list."""
        trigger_object = Trigger(trigger)
        self._trigger = trigger_object
        self._slash_commands = slash_commands

        #self.trigger = trigger_object
        self.slash_commands = slash_commands

    ### Properties
    @property
    def trigger(self) -> str:
        return self._trigger.trigger_string
    
    @trigger.setter
    def trigger(self, trigger_string: str):
        self._trigger = Trigger(trigger_string)

    @property
    def slash_commands(self) -> list[str]:
        return self._slash_commands
    
    @slash_commands.setter
    def slash_commands(self, slash_commands: list[str]):
        self._throw_error_on_invalid_slash_commands(slash_commands = slash_commands)
        self._slash_commands = slash_commands
    
    @property
    def bind_string(self) -> str:
        return self._build_bind_string()
    
    ### Methods
    def set_trigger_modifier(self, modifier: str):
        """Set the trigger modifier."""
        self._trigger.modifier = modifier

    def clear_trigger_modifier(self):
        """Clear the trigger modifier."""
        self._trigger.clear_modifier()

    ### Copy
    def copy(self) -> 'Bind':
        """Return a copy of the bind."""
        return Bind(trigger = deepcopy(self._trigger), 
                    slash_commands = deepcopy(self._slash_commands))

    ### Helpers
    def _build_bind_string(self, slash_commands: list[str] = None) -> str:
        """Helper function to build the bind string."""
        if slash_commands is None:
            slash_commands = self.slash_commands
        return f"{self.trigger} \"{'$$'.join(slash_commands)}\""
    
    def _is_modified_trigger(self, trigger: str) -> bool:
        """Helper function to determine if the trigger contains a modifier."""
        trigger_parts = trigger.split('+')
        return len(trigger_parts) == 2

    ### Error Checking/Validation
    def _throw_error_on_invalid_slash_commands(self, slash_commands: list[str]):
        """Helper function to validate the slash commands."""
        if not slash_commands:
            raise ValueError("Invalid slash commands. Slash Commands list cannot be empty.")
        if not all(slash_commands):
            raise ValueError("Invalid slash commands. Slash Commands list cannot contain empty commands.")

    def is_over_bind_length(self, bind: 'Bind') -> bool:
        """Helper function to ensure the total bind string does not exceed max character length."""
        return len(bind.bind_string) > self.MAX_BIND_LENGTH
    
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
    def __init__(self, trigger: str, 
                 slash_commands: list[str] = [], 
                 toggle_off_powers: list[str] = [], 
                 toggle_on_powers: list[str] = [], 
                 auto_power: str = ""):
        self._toggle_off_powers = toggle_off_powers
        self._toggle_on_powers = toggle_on_powers
        self._auto_power = auto_power
        
        super().__init__(trigger, slash_commands)
        
        self.toggle_off_power = toggle_off_powers
        self.toggle_on_power = toggle_on_powers
        self.auto_power = auto_power

    ### Properties
    @property
    def toggle_off_powers(self) -> list[str]:
        return self._toggle_off_powers
    
    @toggle_off_powers.setter
    def toggle_off_powers(self, toggle_off_powers: list[str]):
        self._throw_error_on_invalid_slash_commands(toggle_off_powers = toggle_off_powers)
        self._toggle_off_powers = toggle_off_powers

    @property
    def toggle_on_powers(self) -> list[str]:
        return self._toggle_on_powers
    
    @toggle_on_powers.setter
    def toggle_on_powers(self, toggle_on_powers: list[str]):
        self._throw_error_on_invalid_slash_commands(toggle_on_powers = toggle_on_powers)
        self._toggle_on_powers = toggle_on_powers

    @property
    def auto_power(self) -> str:
        return self._auto_power
    
    @auto_power.setter
    def auto_power(self, auto_power: str):
        self._throw_error_on_invalid_slash_commands(auto_power = auto_power)
        self._auto_power = auto_power

    ### Copy
    def copy(self) -> 'ToggleBind':
        """Return a copy of the WASD bind."""
        return ToggleBind(trigger = deepcopy(self.trigger), 
                        slash_commands = deepcopy(self.slash_commands), 
                        toggle_off_powers = deepcopy(self.toggle_off_powers), 
                        toggle_on_powers = deepcopy(self.toggle_on_powers), 
                        auto_power = deepcopy(self.auto_power))

    ### Helpers
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        toggle_off_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_OFF} {power.lower()}" for power in self.toggle_off_powers]
        toggle_on_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_ON} {power.lower()}" for power in self.toggle_on_powers]
        combined_slash_commands = toggle_off_slash_commands + toggle_on_slash_commands
        if self.auto_power:
            combined_slash_commands += [f"{SlashCommands.POWEXEC_AUTO} {self.auto_power}"]
        combined_slash_commands += self.slash_commands
        return Bind._build_bind_string(self, combined_slash_commands)
    
    ### Error Checking/Validation
    def _throw_error_on_invalid_slash_commands(self, 
                                               slash_commands: list[str] = None, 
                                               toggle_off_powers: list[str] = None, 
                                               toggle_on_powers: list[str] = None, 
                                               auto_power: str = None):
        if slash_commands is None:
            slash_commands = self._slash_commands
        if toggle_off_powers is None:
            toggle_off_powers = self._toggle_off_powers
        if toggle_on_powers is None:
            toggle_on_powers = self._toggle_on_powers
        if auto_power is None:
            auto_power = self._auto_power

        combined_slash_commands = slash_commands + toggle_off_powers + toggle_on_powers
        if auto_power:
            combined_slash_commands += [auto_power]
        super()._throw_error_on_invalid_slash_commands(combined_slash_commands)

class WASDBind(ToggleBind):
    WASD_TRIGGER_MAP = {
        "W": "+forward",
        "A": "+left",
        "S": "+backward",
        "D": "+right",
        "SPACE": "+up"
    }

    ### Initialization
    def __init__(self, 
                 trigger: str, 
                 slash_commands: list[str] = [],
                 toggle_off_powers: list[str] = [],
                 movement_powers: list[str] = [], 
                 toggle_on_powers: list[str] = [], 
                 auto_power: str = "",):
        """Initialize the WASD bind with a trigger and a default movement slash command."""
        self._movement_powers = movement_powers
        self._direction = ""

        super().__init__(trigger, slash_commands, toggle_off_powers, toggle_on_powers, auto_power)

        self.movement_powers = movement_powers

    ### Properties
    @property
    def trigger(self) -> str:
        return super().trigger
    
    @trigger.setter
    def trigger(self, trigger: str):
        self._throw_error_on_invalid_wasd_trigger(trigger)
        super().trigger = trigger
        self._direction = self._get_wasd_direction(trigger)

    @property
    def movement_powers(self) -> list[str]:
        return self._movement_powers
    
    @movement_powers.setter
    def movement_powers(self, movement_powers: list[str]):
        self._throw_error_on_invalid_slash_commands(movement_powers = movement_powers)
        self._movement_powers = movement_powers
    
    ### Copy
    def copy(self) -> 'WASDBind':
        """Return a copy of the WASD bind."""
        return WASDBind(trigger = deepcopy(self.trigger), 
                        slash_commands = deepcopy(self.slash_commands), 
                        toggle_off_powers = deepcopy(self.toggle_off_powers), 
                        movement_powers = deepcopy(self.movement_powers),
                        toggle_on_powers = deepcopy(self.toggle_on_powers), 
                        auto_power = deepcopy(self.auto_power))

    ### Helpers
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        toggle_off_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_OFF} {power.lower()}" for power in self.toggle_off_powers]
        movement_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_ON} {power.lower()}" for power in self.movement_powers]
        toggle_on_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_ON} {power.lower()}" for power in self.toggle_on_powers]
        combined_slash_commands = [self._direction] + toggle_off_slash_commands + movement_slash_commands + toggle_on_slash_commands
        if self.auto_power:
            combined_slash_commands += [f"{SlashCommands.POWEXEC_AUTO} {self.auto_power}"]
        combined_slash_commands += self.slash_commands
        return Bind._build_bind_string(self, combined_slash_commands)
    
    def _get_wasd_direction(self, trigger: str) -> str:
        """Helper function to get the WASD direction for the trigger."""
        return self.WASD_TRIGGER_MAP[trigger.upper()]
    
    def _throw_error_on_invalid_wasd_trigger(self, trigger: str):
        """Helper function to validate the WASD trigger."""
        if trigger not in self.WASD_TRIGGER_MAP:
            raise ValueError(f"Invalid WASD trigger '{trigger}'. Allowed triggers are {list(self.WASD_TRIGGER_MAP.keys())}.")

    ### Error Checking/Validation
    def _throw_error_on_invalid_slash_commands(self, 
                                               slash_commands: list[str] = None, 
                                               toggle_off_powers: list[str] = None,
                                               movement_powers: list[str] = None,
                                               toggle_on_powers: list[str] = None, 
                                               auto_power: str = None):
        if slash_commands is None:
            slash_commands = self._slash_commands
        if toggle_off_powers is None:
            toggle_off_powers = self._toggle_off_powers
        if movement_powers is None:
            movement_powers = self._movement_powers
        if toggle_on_powers is None:
            toggle_on_powers = self._toggle_on_powers
        if auto_power is None:
            auto_power = self._auto_power

        combined_slash_commands = slash_commands + toggle_off_powers + toggle_on_powers + movement_powers
        if auto_power:
            combined_slash_commands += [auto_power]
        Bind._throw_error_on_invalid_slash_commands(self, combined_slash_commands)

    def _throw_error_on_invalid_trigger(self, trigger: str):
        """Helper function to check if the trigger is valid."""
        super()._throw_error_on_invalid_trigger(trigger)
        if trigger.upper() not in self.WASD_TRIGGER_MAP:
            raise ValueError(f"Error: Invalid WASD trigger '{trigger}'. Allowed triggers are {self.WASD_TRIGGER_MAP.keys}.")