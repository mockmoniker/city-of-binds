from CityOfBinds.slashcommand import SlashCommand
from CityOfBinds.power import Power

class CommandGroupConstants:
    """Constants for command group operations."""
    COMMAND_DELIM = "$$"

    # Power execution commands
    POWEXEC_NAME = "powexecname"
    POWEXEC_TOGGLE_OFF = "powexectoggleoff"
    POWEXEC_TOGGLE_ON = "powexectoggleon"
    POWEXEC_AUTO = "powexecauto"
    POWEXEC_LOCATION = "powexeclocation"

    # Location power arguments
    LOCATION_SELF = "me"
    LOCATION_TARGET = "target"
    LOCATION_CURSOR = "cursor"

    # Bind file commands
    BIND_LOAD = "bindload"
    BIND_LOAD_FILE = "bindloadfile"
    BIND_LOAD_FILE_SILENT = "bindloadfilesilent"
    BIND_SAVE = "bindsave"
    BIND_SAVE_FILE = "bindsavefile"
    BIND_SAVE_FILE_SILENT = "bindsavefilesilent"

    # Emote commands
    EMOTE = "e"
    CC_EMOTE = "cce"

    # Movement commands
    DIRECTION_TO_MOVEMENT_MAP = {
        "forward": "+forward",
        "left": "+left",
        "backward": "+backward",
        "right": "+right",
        "up": "+up",
    }

class CommandGroup:
    """A class representing a group of commands"""
    def __init__(self, commands_string_list: list[str] = None):
        self._commands = [SlashCommand(command) for command in commands_string_list] if commands_string_list is not None else []

    # region Basic Command Methods
    def add_command(self, command_string: str) -> 'CommandGroup':
        """Add a command to the command group."""
        return self.insert_command(len(self._commands), command_string)

    def prepend_command(self, command_string: str) -> 'CommandGroup':
        """Prepend a command to the command group."""
        return self.insert_command(0, command_string)
    
    def insert_command(self, index: int, command_string: str) -> 'CommandGroup':
        """Insert a command at a specific index in the command group."""
        command = SlashCommand(command_string)
        self._commands.insert(index, command)
        return self

    def clear_commands(self) -> 'CommandGroup':
        """Clear all commands from the command group."""
        self._commands.clear()
        return self
    
    # endregion

    # region Power Command Methods
    def add_power(self, power_string: str) -> 'CommandGroup':
        """Add a power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_NAME, power_string)

    def add_toggle_on_power(self, power_string: str) -> 'CommandGroup':
        """Add a toggle on power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_TOGGLE_ON, power_string)
    
    def add_toggle_off_power(self, power_string: str) -> 'CommandGroup':
        """Add a toggle off power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_TOGGLE_OFF, power_string)

    def add_auto_power(self, power_string: str) -> 'CommandGroup':
        """Add an auto power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_AUTO, power_string)

    def add_loc_self_power(self, power_string: str) -> 'CommandGroup':
        """Add a locational power on self as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_LOCATION, power_string, CommandGroupConstants.LOCATION_SELF)
    
    def add_loc_target_power(self, power_string: str) -> 'CommandGroup':
        """Add a locational power on target as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_LOCATION, power_string, CommandGroupConstants.LOCATION_TARGET)

    def add_loc_cursor_power(self, power_string: str) -> 'CommandGroup':
        """Add a locational power on cursor as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_LOCATION, power_string, CommandGroupConstants.LOCATION_CURSOR)
    
    def _add_power_command(self, powexec_type: str, power_string: str, location_arg: str = None) -> 'CommandGroup':
        """Helper function to add a power command to the command group."""
        power = Power(power_string)
        if location_arg:
            command_string = f"{powexec_type} {location_arg} {str(power)}"
        else:
            command_string = f"{powexec_type} {str(power)}"
        return self.add_command(command_string)
    
    # endregion

    # region Movement Command Methods
    def prepend_movement(self, direction_string: str) -> 'CommandGroup':
        """Prepend a movement command to the command group."""
        direction = direction_string.lower()
        self._throw_error_if_wrong_direction(direction)
        movement_command = CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP[direction]
        return self.prepend_command(movement_command)
    
    # endregion

    def add_bind_load(self) -> 'CommandGroup':
        """Add a bind load command as a slash command to the command group."""
        return self.add_command(CommandGroupConstants.BIND_LOAD)

    def add_bind_load_file(self, file_path: str, is_silent: bool = False) -> 'CommandGroup':
        """Add a bind load file command as a slash command to the command group."""
        command_string = f"{CommandGroupConstants.BIND_LOAD_FILE_SILENT if is_silent else CommandGroupConstants.BIND_LOAD_FILE} {file_path}"
        return self.add_command(command_string)

    def add_bind_save(self) -> 'CommandGroup':
        """Add a bind save command as a slash command to the command group."""
        return self.add_command(CommandGroupConstants.BIND_SAVE)
    
    def add_bind_save_file(self, file_path: str, is_silent: bool = False) -> 'CommandGroup':
        """Add a bind save file command as a slash command to the command group."""
        command_string = f"{CommandGroupConstants.BIND_SAVE_FILE_SILENT if is_silent else CommandGroupConstants.BIND_SAVE_FILE} {file_path}"
        return self.add_command(command_string)

    def add_emote(self, emote_string: str) -> 'CommandGroup':
        """Add an emote command as a slash command to the command group."""
        return self.add_command(f"{CommandGroupConstants.EMOTE} {emote_string}")

    def add_cc_emote(self, emote_string: str, cc_slot: int) -> 'CommandGroup':
        """Add a CC emote command as a slash command to the command group."""
        if cc_slot < 0 or cc_slot > 9:
            raise ValueError("CC slot must be between 0 and 9.")
        return self.add_command(f"{CommandGroupConstants.CC_EMOTE} {cc_slot} {emote_string}")

    ### Helpers
    
    
    ### Error Checking/Validation
    def _throw_error_if_wrong_direction(self, direction_string: str):
        """Helper function to ensure the movement direction is valid."""
        if direction_string not in CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP:
            raise ValueError(f"Invalid movement direction: '{direction_string}', valid directions are: {', '.join(CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP.keys())}")

    ### Dunder Methods
    def __iter__(self):
        return iter(self._commands)
    
    def __getitem__(self, index):
        return self._commands[index]
    
    def __setitem__(self, index, value):
        self._commands[index] = SlashCommand(value)

    def __len__(self):
        return len(self._commands)
    
    def __add__(self, other: 'CommandGroup') -> 'CommandGroup':
        new_command_group = CommandGroup()
        new_command_group._commands = self._commands + other._commands
        return new_command_group
    
    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, CommandGroup):
            return False
        if len(self) != len(other):
            return False
        for cmd_self, cmd_other in zip(self, other):
            if cmd_self != cmd_other:
                return False
        return True
    
    def __str__(self) -> str:
        """Override the default string representation."""
        return f"\"{CommandGroupConstants.COMMAND_DELIM.join(str(command) for command in self._commands)}\""