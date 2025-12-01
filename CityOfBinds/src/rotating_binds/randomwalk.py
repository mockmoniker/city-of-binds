import random
from CityOfBinds.src.binds.bind import Bind
from CityOfBinds.src.slash_commands.slashcommand import Commands
from CityOfBinds.src.bind_file.bindfile import BindFile, BindFileNode, BindFileGraph
from CityOfBinds.src.bind_fileGraphPublisher.publisher import BFGPublisher


class RandomWalk(BFGPublisher):

    def __init__(
        self, wasd_template: list = None, jump_template: list = None, *args, **kwargs
    ):
        self.wasd_template = wasd_template
        self.jump_template = jump_template

    def _build_binds(self, trigger, template):
        # Implementation to build binds based on the trigger and template
        pass

    def _create_nodes(self) -> list[BindFileNode]:
        pass
