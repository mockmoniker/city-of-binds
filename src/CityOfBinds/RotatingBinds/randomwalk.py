import random
from CityOfBinds.binds import Bind
from CityOfBinds.slashcommand import Commands
from CityOfBinds.bindfile import BindFile, BindFileNode, BindFileGraph

class RandomWalk:

    def __init__(self, actions: list[Commands]):
        self.actions = actions

    def _create_nodes(self) -> list[BindFileNode]:
        pass