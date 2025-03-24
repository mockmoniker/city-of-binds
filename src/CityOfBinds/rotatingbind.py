from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile

class RotatingBind(Bind):
    def __init__(self, trigger: str, slash_commands_rotations: list[list[str]]):
        """Initialize the rotating bind with a list of binds."""
        self._binds = binds
        self._current_bind_index = 0