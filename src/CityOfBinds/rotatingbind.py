from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile

class RotatingBind(Bind):
    def __init__(self, trigger: str, slash_commands_rotations: list[list[str]], rotation_prefix: str = ""):
        self._rotation_prefix = rotation_prefix
        self._slash_commands_rotations = slash_commands_rotations

        super().__init__(trigger = trigger, slash_commands=["nop"])

        self.rotation_prefix = rotation_prefix
        self.slash_commands_rotations = slash_commands_rotations

    ### Properties
    @property
    def slash_commands(self) -> list[str]:
        self._throw_error_on_unsupported_slash_commands()
    
    @slash_commands.setter
    def slash_commands(self, slash_commands: list[str]):
        self._throw_error_on_unsupported_slash_commands()

    @property
    def rotation_prefix(self) -> str:
        return self._rotation_prefix
    
    @rotation_prefix.setter
    def rotation_prefix(self, rotation_prefix: str):
        self._throw_error_on_invalid_prefix(rotation_prefix)
        self._rotation_prefix = rotation_prefix

    @property
    def slash_commands_rotations(self) -> list[list[str]]:
        return self._slash_commands_rotations
    
    @slash_commands_rotations.setter
    def slash_commands_rotations(self, slash_commands_rotations: list[list[str]]):
        self._throw_error_on_invalid_slash_commands_rotations(slash_commands_rotations)
        self._slash_commands_rotations = slash_commands_rotations

    @property
    def bind_string(self) -> list[str]:
        return [self._build_bind_string(slash_commands) for slash_commands in self._slash_commands_rotations]

    ### Error Checking/Validation
    def _throw_error_on_unsupported_slash_commands(self):
        raise ValueError('RotatingBind does not support \'slash_commands\'. Use \'slash_commands_rotations\' instead.')
    
    def _throw_error_on_invalid_prefix(self, rotation_prefix: str):
        if " " in rotation_prefix:
            raise ValueError(f"Error: Invalid rotation prefix '{rotation_prefix}'. Rotation prefix cannot contain spaces.")

    def _throw_error_on_invalid_slash_commands_rotations(self, slash_commands_rotations: list[list[str]]):
        if not slash_commands_rotations:
            raise ValueError("Error: Slash Commands Rotations list cannot be empty.")
        for slash_commands in slash_commands_rotations:
            super()._throw_error_on_invalid_slash_commands(slash_commands)