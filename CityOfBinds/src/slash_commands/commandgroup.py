from typing import Self
from CityOfBinds.src.slash_commands.slashcommand import SlashCommand
from CityOfBinds.src.slash_commands.power import Power


class _CommandList:
    def __init__(self, commands: list[SlashCommand | str] = None):
        self._commands = (
            [SlashCommand(command) for command in commands]
            if commands is not None
            else []
        )

    # region Basic List Methods
    def add_command(
        self, command_string: str
    ) -> (
        Self
    ):  # TODO: make this the only modification method, prepend and insert aren't necessary (2025/11/29)
        """Add a command to the command group."""
        return self._do_list_method("append", command_string)

    def prepend_command(self, command_string: str) -> Self:
        """Prepend a command to the command group."""
        return self._do_list_method("insert", 0, command_string)

    def insert_command(self, index: int, command_string: str) -> Self:
        """Insert a command at a specific index in the command group."""
        return self._do_list_method("insert", index, command_string)

    def clear_commands(self) -> Self:
        """Clear all commands from the command group."""
        return self._do_list_method("clear")

    def _do_list_method(
        self, list_method_name: str, *args, command_string: str = None
    ) -> Self:
        """Modify the command list using a modification function."""
        method = getattr(self._commands, list_method_name)
        if command_string is not None:
            method(*args, SlashCommand(command_string))
        else:
            method(*args)
        return self

    # endregion

    # region Power Command Methods
    def add_power(self, power_string: str) -> Self:
        """Add a power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_NAME, power_string)

    def add_toggle_on_power(self, power_string: str) -> Self:
        """Add a toggle on power as a slash command to the command group."""
        return self._add_power_command(
            CommandGroupConstants.POWEXEC_TOGGLE_ON, power_string
        )

    def add_toggle_off_power(self, power_string: str) -> Self:
        """Add a toggle off power as a slash command to the command group."""
        return self._add_power_command(
            CommandGroupConstants.POWEXEC_TOGGLE_OFF, power_string
        )

    def add_auto_power(self, power_string: str) -> Self:
        """Add an auto power as a slash command to the command group."""
        return self._add_power_command(CommandGroupConstants.POWEXEC_AUTO, power_string)

    def add_loc_self_power(self, power_string: str) -> Self:
        """Add a locational power on self as a slash command to the command group."""
        return self._add_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_SELF,
        )

    def add_loc_target_power(self, power_string: str) -> Self:
        """Add a locational power on target as a slash command to the command group."""
        return self._add_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_TARGET,
        )

    def add_loc_cursor_power(self, power_string: str) -> Self:
        """Add a locational power on cursor as a slash command to the command group."""
        return self._add_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_CURSOR,
        )

    def prepend_power(self, power_string: str) -> Self:
        """Prepend a power as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_NAME, power_string
        )

    def prepend_toggle_on_power(self, power_string: str) -> Self:
        """Prepend a toggle on power as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_TOGGLE_ON, power_string
        )

    def prepend_toggle_off_power(self, power_string: str) -> Self:
        """Prepend a toggle off power as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_TOGGLE_OFF, power_string
        )

    def prepend_auto_power(self, power_string: str) -> Self:
        """Prepend an auto power as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_AUTO, power_string
        )

    def prepend_loc_self_power(self, power_string: str) -> Self:
        """Prepend a locational power on self as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_SELF,
        )

    def prepend_loc_target_power(self, power_string: str) -> Self:
        """Prepend a locational power on target as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_TARGET,
        )

    def prepend_loc_cursor_power(self, power_string: str) -> Self:
        """Prepend a locational power on cursor as a slash command to the command group."""
        return self._prepend_power_command(
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_CURSOR,
        )

    def insert_power(self, index: int, power_string: str) -> Self:
        """Insert a power at a specific index in the command group."""
        return self._insert_power_command(
            index, CommandGroupConstants.POWEXEC_NAME, power_string
        )

    def insert_toggle_on_power(self, index: int, power_string: str) -> Self:
        """Insert a toggle on power at a specific index in the command group."""
        return self._insert_power_command(
            index, CommandGroupConstants.POWEXEC_TOGGLE_ON, power_string
        )

    def insert_toggle_off_power(self, index: int, power_string: str) -> Self:
        """Insert a toggle off power at a specific index in the command group."""
        return self._insert_power_command(
            index, CommandGroupConstants.POWEXEC_TOGGLE_OFF, power_string
        )

    def insert_auto_power(self, index: int, power_string: str) -> Self:
        """Insert an auto power at a specific index in the command group."""
        return self._insert_power_command(
            index, CommandGroupConstants.POWEXEC_AUTO, power_string
        )

    def insert_loc_self_power(self, index: int, power_string: str) -> Self:
        """Insert a locational power on self at a specific index in the command group."""
        return self._insert_power_command(
            index,
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_SELF,
        )

    def insert_loc_target_power(self, index: int, power_string: str) -> Self:
        """Insert a locational power on target at a specific index in the command group."""
        return self._insert_power_command(
            index,
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_TARGET,
        )

    def insert_loc_cursor_power(self, index: int, power_string: str) -> Self:
        """Insert a locational power on cursor at a specific index in the command group."""
        return self._insert_power_command(
            index,
            CommandGroupConstants.POWEXEC_LOCATION,
            power_string,
            CommandGroupConstants.LOCATION_CURSOR,
        )

    def _add_power_command(
        self, powexec_type: str, power_string: str, location_arg: str = None
    ) -> Self:
        """Helper function to add a power command to the command group."""
        command_string = self._build_power_command_string(
            powexec_type, power_string, location_arg
        )
        return self.add_command(command_string)

    def _prepend_power_command(
        self, powexec_type: str, power_string: str, location_arg: str = None
    ) -> Self:
        """Helper function to prepend a power command to the command group."""
        command_string = self._build_power_command_string(
            powexec_type, power_string, location_arg
        )
        return self.prepend_command(command_string)

    def _insert_power_command(
        self, index: int, powexec_type: str, power_string: str, location_arg: str = None
    ) -> Self:
        """Helper function to insert a power command at a specific index in the command group."""
        command_string = self._build_power_command_string(
            powexec_type, power_string, location_arg
        )
        return self.insert_command(index, command_string)

    def _build_power_command_string(
        self, powexec_type: str, power_string: str, argument: str = None
    ) -> str:
        """Helper function to build a power command string."""
        power = Power(power_string)
        if argument:
            return f"{powexec_type} {argument} {str(power)}"
        return f"{powexec_type} {str(power)}"

    # endregion

    # region Movement Command Methods
    def add_movement(self, direction_string: str) -> Self:
        """Add a movement command to the command group."""
        return self._add_movement_command(direction_string)

    def prepend_movement(self, direction_string: str) -> Self:
        """Prepend a movement command to the command group."""
        return self._prepend_movement_command(direction_string)

    def insert_movement(self, index: int, direction_string: str) -> Self:
        """Insert a movement command at a specific index in the command group."""
        return self._insert_movement_command(index, direction_string)

    def _add_movement_command(self, direction_string: str) -> Self:
        """Add a movement command to the command group."""
        command_string = self._build_movement_command_string(direction_string)
        return self.add_command(command_string)

    def _prepend_movement_command(self, direction_string: str) -> Self:
        """Prepend a movement command to the command group."""
        command_string = self._build_movement_command_string(direction_string)
        return self.prepend_command(command_string)

    def _insert_movement_command(self, index: int, direction_string: str) -> Self:
        """Insert a movement command at a specific index in the command group."""
        command_string = self._build_movement_command_string(direction_string)
        return self.insert_command(index, command_string)

    def _build_movement_command_string(self, direction_string: str) -> str:
        direction = direction_string.lower()
        self._throw_error_if_wrong_direction(direction)
        return CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP[direction]

    def _throw_error_if_wrong_direction(self, direction_string: str):
        """Helper function to ensure the movement direction is valid."""
        if direction_string not in CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP:
            raise ValueError(
                f"Invalid movement direction: '{direction_string}', valid directions are: {', '.join(CommandGroupConstants.DIRECTION_TO_MOVEMENT_MAP.keys())}"
            )

    # endregion

    # region Bind File Command Methods
    def add_bind_load(self) -> Self:
        """Add a bind load command as a slash command to the command group."""
        return self.add_command(CommandGroupConstants.BIND_LOAD)

    def add_bind_load_file(self, file_path: str) -> Self:
        """Add a bind load file command as a slash command to the command group."""
        return self._add_bind_file_command(
            CommandGroupConstants.BIND_LOAD_FILE, file_path
        )

    def add_bind_load_file_silent(self, file_path: str) -> Self:
        """Add a bind load file silent command as a slash command to the command group."""
        return self._add_bind_file_command(
            CommandGroupConstants.BIND_LOAD_FILE_SILENT, file_path
        )

    def add_bind_save(self) -> Self:
        """Add a bind save command as a slash command to the command group."""
        return self.add_command(CommandGroupConstants.BIND_SAVE)

    def add_bind_save_file(self, file_path: str) -> Self:
        """Add a bind save file command as a slash command to the command group."""
        return self._add_bind_file_command(
            CommandGroupConstants.BIND_SAVE_FILE, file_path
        )

    def add_bind_save_file_silent(self, file_path: str) -> Self:
        """Add a bind save file silent command as a slash command to the command group."""
        return self._add_bind_file_command(
            CommandGroupConstants.BIND_SAVE_FILE_SILENT, file_path
        )

    def prepend_bind_load(self) -> Self:
        """Prepend a bind load command as a slash command to the command group."""
        return self.prepend_command(CommandGroupConstants.BIND_LOAD)

    def prepend_bind_load_file(self, file_path: str) -> Self:
        """Prepend a bind load file command as a slash command to the command group."""
        return self._prepend_bind_file_command(
            CommandGroupConstants.BIND_LOAD_FILE, file_path
        )

    def prepend_bind_load_file_silent(self, file_path: str) -> Self:
        """Prepend a bind load file silent command as a slash command to the command group."""
        return self._prepend_bind_file_command(
            CommandGroupConstants.BIND_LOAD_FILE_SILENT, file_path
        )

    def prepend_bind_save(self) -> Self:
        """Prepend a bind save command as a slash command to the command group."""
        return self.prepend_command(CommandGroupConstants.BIND_SAVE)

    def prepend_bind_save_file(self, file_path: str) -> Self:
        """Prepend a bind save file command as a slash command to the command group."""
        return self._prepend_bind_file_command(
            CommandGroupConstants.BIND_SAVE_FILE, file_path
        )

    def prepend_bind_save_file_silent(self, file_path: str) -> Self:
        """Prepend a bind save file silent command as a slash command to the command group."""
        return self._prepend_bind_file_command(
            CommandGroupConstants.BIND_SAVE_FILE_SILENT, file_path
        )

    def insert_bind_load(self, index: int) -> Self:
        """Insert a bind load command as a slash command to the command group."""
        return self.insert_command(index, CommandGroupConstants.BIND_LOAD)

    def insert_bind_load_file(self, index: int, file_path: str) -> Self:
        """Insert a bind load file command as a slash command to the command group."""
        return self._insert_bind_file_command(
            index, CommandGroupConstants.BIND_LOAD_FILE, file_path
        )

    def insert_bind_load_file_silent(self, index: int, file_path: str) -> Self:
        """Insert a bind load file silent command as a slash command to the command group."""
        return self._insert_bind_file_command(
            index, CommandGroupConstants.BIND_LOAD_FILE_SILENT, file_path
        )

    def insert_bind_save(self, index: int) -> Self:
        """Insert a bind save command as a slash command to the command group."""
        return self.insert_command(index, CommandGroupConstants.BIND_SAVE)

    def insert_bind_save_file(self, index: int, file_path: str) -> Self:
        """Insert a bind save file command as a slash command to the command group."""
        return self._insert_bind_file_command(
            index, CommandGroupConstants.BIND_SAVE_FILE, file_path
        )

    def insert_bind_save_file_silent(self, index: int, file_path: str) -> Self:
        """Insert a bind save file silent command as a slash command to the command group."""
        return self._insert_bind_file_command(
            index, CommandGroupConstants.BIND_SAVE_FILE_SILENT, file_path
        )

    def _add_bind_file_command(
        self, bind_file_command: str, bind_file_path: str
    ) -> Self:
        """Helper function to add a bind file command to the command group."""
        command_string = self._build_bind_file_command_string(
            bind_file_command, bind_file_path
        )
        return self.add_command(command_string)

    def _prepend_bind_file_command(
        self, bind_file_command: str, bind_file_path: str
    ) -> Self:
        """Helper function to prepend a bind file command to the command group."""
        command_string = self._build_bind_file_command_string(
            bind_file_command, bind_file_path
        )
        return self.prepend_command(command_string)

    def _insert_bind_file_command(
        self, index: int, bind_file_command: str, bind_file_path: str
    ) -> Self:
        """Helper function to insert a bind file command at a specific index in the command group."""
        command_string = self._build_bind_file_command_string(
            bind_file_command, bind_file_path
        )
        return self.insert_command(index, command_string)

    def _build_bind_file_command_string(
        self, bind_file_command: str, bind_file_path: str
    ) -> str:
        return f"{bind_file_command} {bind_file_path}"

    # endregion

    def add_emote(self, emote_string: str) -> Self:
        """Add an emote command as a slash command to the command group."""
        return self.add_command(f"{CommandGroupConstants.EMOTE} {emote_string}")

    def add_cc_emote(self, emote_string: str, cc_slot: int) -> Self:
        """Add a CC emote command as a slash command to the command group."""
        if cc_slot < 0 or cc_slot > 9:
            raise ValueError("CC slot must be between 0 and 9.")
        return self.add_command(
            f"{CommandGroupConstants.CC_EMOTE} {cc_slot} {emote_string}"
        )

    # region Dunder Methods
    def __iter__(self):
        return iter(self._commands)

    def __getitem__(self, index):
        return self._commands[index]

    def __setitem__(self, index, value):
        self._commands[index] = SlashCommand(value)

    def __len__(self):
        return len(self._commands)

    def __add__(self, other: "_CommandList") -> Self:
        new_command_group = self.__class__()  # Creates same type as caller
        new_command_group._commands = self._commands + other._commands
        return new_command_group

    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, _CommandList):
            return False
        if len(self) != len(other):
            return False
        for cmd_self, cmd_other in zip(self, other):
            if str(cmd_self) != str(cmd_other):
                return False
        return True

    # endregion


class CommandGroupConstants:
    """Constants for command group operations."""

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
    BIND_SAVE = "bindsave"  # TODO: verify if these commands still work. Should be show_bind_file? (2025/11/28)
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


class CommandGroup(_CommandList):
    COMMAND_DELIM = "$$"

    """A class representing a group of commands"""

    def __init__(self, commands: list[SlashCommand | str] = None):
        super().__init__(commands)

    # region Dunder Methods
    def __str__(self) -> str:
        """Override the default string representation."""
        return (
            f'"{self.COMMAND_DELIM.join(str(command) for command in self._commands)}"'
        )

    # endregion
