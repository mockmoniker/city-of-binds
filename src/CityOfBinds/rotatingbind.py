from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile

class RotatingBind():
    def __init__(self, bindfile: BindFile):
        """Initialize the rotating bind with a bind file."""
        self.bindfile = bindfile