from copy import deepcopy
from typing import Union, Callable
from CityOfBinds.slashcommands import SlashCommands

class Bind:
    MAX_BIND_LENGTH = 255

    ### Initialization
    def __init__(self, trigger: str, slash_commands: Union[str, list[str]]):
        """Initialize the bind with a trigger and slash command list."""
        self.trigger: str = ""
        self.slash_commands: list[str] = []

        self._set_trigger(trigger)
        if isinstance(slash_commands, str):
            self._add_slash_command(slash_commands)
        else:
            self._add_slash_commands(slash_commands)

        self._check_will_exceed_max_length(self)

    ### Setters
    def set_trigger(self, trigger: str):
        """Set the trigger of the bind. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(Bind._set_trigger, trigger)
        self._set_trigger(trigger)

    def _set_trigger(self, trigger: str):
        """Helper function to set the trigger."""
        self.trigger = trigger

    def set_slash_command(self, slash_command: str):
        """Set the slash command of the bind. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(Bind._set_slash_command, slash_command)
        self._set_slash_command(slash_command)

    def _set_slash_command(self, slash_command: str):
        """Helper function to set the slash command."""
        self.slash_commands = [slash_command]

    def set_slash_commands(self, slash_commands: Union[str, list[str]]):
        """Set the slash commands of the bind. Ensure the total bind string does not exceed max character length."""
        if isinstance(slash_commands, str):
            self.set_slash_command(slash_commands)
            return
        self._check_potential_action(Bind._set_slash_commands, slash_commands)
        self._set_slash_commands(slash_commands)

    def _set_slash_commands(self, slash_commands: list[str]):
        """Helper function to set the slash commands."""
        self.slash_commands = slash_commands

    ### Adders
    def add_slash_command(self, slash_command: str):
        """Add a command to the bind. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(Bind._add_slash_command, slash_command)
        self._add_slash_command(slash_command)

    def _add_slash_command(self, slash_command: str):
        """Helper function to add a slash command."""
        self.slash_commands.append(slash_command)

    def add_slash_commands(self, slash_commands: Union[str, list[str]]):
        """Add a list of commands to the bind. Ensure the total bind string does not exceed max character length."""
        if isinstance(slash_commands, str):
            self.add_slash_command(slash_commands)
            return
        self._check_potential_action(Bind._add_slash_commands, slash_commands)
        self._add_slash_commands(slash_commands)

    def _add_slash_commands(self, slash_commands: list[str]):
        """Helper function to add a list of slash commands."""
        self.slash_commands.extend(slash_commands)

    ### Getters
    def get_trigger(self) -> str:
        """Return the trigger of the bind."""
        return self.trigger.upper()
    
    def get_bind_string(self) -> str:
        """Return the complete bind string."""
        return self._build_bind_string()
    
    ### Copy
    def copy(self) -> 'Bind':
        """Return a copy of the bind."""
        return Bind(trigger = deepcopy(self.trigger), 
                    slash_commands = deepcopy(self.slash_commands))

    ### Helpers
    def _build_bind_string(self, slash_commands: list[str] = None) -> str:
        """Helper function to build the bind string."""
        if slash_commands is None:
            slash_commands = self.slash_commands
        return f"{self.get_trigger()} \"{'$$'.join(slash_commands)}\""
    
    ### Error Checking/Validation
    def _check_potential_action(self, potential_action: Callable[['Bind', Union[str, list[str]]], None], potential_action_args: Union[str, list[str]]):
        """Helper function to perform the potential action on a copy of the current object."""
        potential_bind = self.copy()
        potential_action(potential_bind, potential_action_args)
        self._check_will_exceed_max_length(potential_bind)
        del potential_bind

    def _check_will_exceed_max_length(self, potential_bind: 'Bind'):
        """Helper function to ensure the total bind string does not exceed max character length."""
        if len(potential_bind._build_bind_string()) > self.MAX_BIND_LENGTH:
            raise ValueError(f"Error: The bind string '{potential_bind._build_bind_string()}' exceeds the maximum length of {self.MAX_BIND_LENGTH} characters.")

class WASDBind(Bind):
    ALLOWED_TRIGGERS = ["W", "A", "S", "D", "SPACE"]
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
                 slash_commands: Union[str, list[str]] = [], 
                 toggle_off_powers: Union[str, list[str]] = [], 
                 toggle_on_powers: Union[str, list[str]] = [], 
                 auto_power: str = ""):
        """Initialize the WASD bind with a trigger and a default movement slash command."""
        self.toggle_off_powers: list[str] = []
        self.toggle_on_powers: list[str] = []
        self.auto_power: str = ""

        self._check_valid_wasd_trigger(trigger)
        
        self._set_toggle_off_powers(toggle_off_powers)
        self._set_toggle_on_powers(toggle_on_powers)
        self._set_auto_power(auto_power)

        super().__init__(trigger, slash_commands)

    ### Setters
    def set_trigger(self, trigger: str):
        """Set the trigger of the WASD bind. Ensure the total bind string does not exceed max character length."""
        self._check_valid_wasd_trigger(trigger)
        self._check_potential_action(WASDBind._set_trigger, trigger)
        self._set_trigger(trigger)

    def _set_trigger(self, trigger: str): 
        """Helper function to set the trigger of the WASD bind."""
        super()._set_trigger(trigger)
        if not self.slash_commands:
            self._add_slash_command(self._get_wasd_direction(trigger))
        else:
            self.slash_commands[0] = self._get_wasd_direction(trigger)

    def set_toggle_off_power(self, toggle_off_power: str):
        """Set the toggle off power. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(WASDBind._set_toggle_off_power, toggle_off_power)
        self._set_toggle_off_power(toggle_off_power)

    def _set_toggle_off_power(self, toggle_off_power: str):
        """Helper function to set the toggle off power."""
        self.toggle_off_powers = [toggle_off_power]

    def set_toggle_off_powers(self, toggle_off_powers: Union[str, list[str]]):
        """Helper function to set the toggle off list."""
        if isinstance(toggle_off_powers, str):
            self.set_toggle_off_power(toggle_off_powers)
            return
        self._check_potential_action(WASDBind._set_toggle_off_powers, toggle_off_powers)
        self.toggle_off_powers = toggle_off_powers

    def _set_toggle_off_powers(self, toggle_off_powers: list[str]):
        """Helper function to set the toggle off list."""
        self.toggle_off_powers = toggle_off_powers

    def set_toggle_on_power(self, toggle_on_power: str):
        """Set the toggle on power. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(WASDBind._set_toggle_on_power, toggle_on_power)
        self._set_toggle_on_power(toggle_on_power)

    def _set_toggle_on_power(self, toggle_on_power: str):
        """Helper function to set the toggle on power."""
        self.toggle_on_powers = [toggle_on_power]

    def set_toggle_on_powers(self, toggle_on_powers: Union[str, list[str]]):
        """Set the toggle on list. Ensure the total bind string does not exceed max character length."""
        if isinstance(toggle_on_powers, str):
            self.set_toggle_on_power(toggle_on_powers)
            return
        self._check_potential_action(WASDBind._set_toggle_on_powers, toggle_on_powers)
        self._set_toggle_on_powers(toggle_on_powers)
    
    def _set_toggle_on_powers(self, toggle_on_powers: list[str]):
        """Helper function to set the toggle on list."""
        self.toggle_on_powers = toggle_on_powers

    def set_auto_power(self, power: str):
        """Sets the auto power. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(WASDBind._set_auto_power, power)
        self._set_auto_power(power)

    def _set_auto_power(self, auto_power: str): 
        """Helper function to set the auto rotate command."""
        self.auto_power = auto_power

    ### Adders
    def add_toggle_off_power(self, power: str):
        """Add a power to the toggle off powers list. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(WASDBind._add_toggle_off_power, power)
        self._add_toggle_off_power(power)

    def _add_toggle_off_power(self, power: str):
        """Helper function to add a power to the toggle off powers list."""
        self.toggle_off_powers.append(power)

    def add_toggle_off_powers(self, powers: Union[str, list[str]]):
        """Add a list of poewrs to the toggle off powers list. Ensure the total bind string does not exceed max character length."""
        if isinstance(powers, str):
            self.add_toggle_off_power(powers)
            return
        self._check_potential_action(WASDBind._add_toggle_off_powers, powers)
        self._add_toggle_off_powers(powers)

    def _add_toggle_off_powers(self, powers: list[str]):
        """Helper function to add a list of powers to the toggle off powers list."""
        self.toggle_off_powers.extend(powers)

    def add_toggle_on_power(self, power: str):
        """Add a power to the toggle on power list. Ensure the total bind string does not exceed max character length."""
        self._check_potential_action(WASDBind._add_toggle_on_power, power)
        self._add_toggle_on_power(power)

    def _add_toggle_on_power(self, power: str):
        """Helper function to add a power to the toggle on powers list."""
        self.toggle_on_powers.append(power)

    def add_toggle_on_powers(self, powers: Union[str, list[str]]):
        """Add a list of powers to the toggle on powers list. Ensure the total bind string does not exceed max character length."""
        if isinstance(powers, str):
            self.add_toggle_on_power(powers)
            return
        self._check_potential_action(WASDBind._add_toggle_on_powers, powers)
        self._add_toggle_on_powers(powers)

    def _add_toggle_on_powers(self, powers: list[str]):
        """Helper function to add a list of powers to the toggle on powers list."""
        self.toggle_on_powers.extend(powers)

    ### Clearers
    def clear_toggle_off_powers(self):
        """Clear the toggle off powers list."""
        self.toggle_off_powers.clear()

    def clear_toggle_on_powers(self):
        """Clear the toggle on powers list."""
        self.toggle_on_powers.clear()

    def clear_auto_power(self):
        """Clear the auto power."""
        self.auto_power = ""
    
    ### Copy
    def copy(self) -> 'WASDBind':
        """Return a copy of the WASD bind."""
        return WASDBind(trigger = deepcopy(self.trigger), 
                        slash_commands = deepcopy(self.slash_commands), 
                        toggle_off_powers = deepcopy(self.toggle_off_powers), 
                        toggle_on_powers = deepcopy(self.toggle_on_powers), 
                        auto_power = deepcopy(self.auto_power))

    ### Helpers
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        toggle_off_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_OFF} {power.lower()}" for power in self.toggle_off_powers]
        toggle_on_slash_commands = [f"{SlashCommands.POWEXEC_TOGGLE_ON} {power.lower()}" for power in self.toggle_on_powers]
        combined_slash_commands = [self.slash_commands[0]] + toggle_off_slash_commands + toggle_on_slash_commands
        if self.auto_power:
            combined_slash_commands.append(f"{SlashCommands.POWEXEC_AUTO} {self.auto_power}")
        combined_slash_commands.extend(self.slash_commands[1:])
        return super()._build_bind_string(combined_slash_commands)
    
    def _get_wasd_direction(self, trigger: str) -> str:
        """Helper function to get the WASD direction for the trigger."""
        return self.WASD_TRIGGER_MAP[trigger.upper()]

    ### Error Checking/Validation
    def _check_valid_wasd_trigger(self, trigger: str):
        """Helper function to check if the trigger is valid."""
        if trigger.upper() not in self.ALLOWED_TRIGGERS:
            raise ValueError(f"Invalid trigger '{trigger}'. Allowed triggers are {self.ALLOWED_TRIGGERS}.")