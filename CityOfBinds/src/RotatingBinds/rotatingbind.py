from CityOfBinds.src.Binds.bind import Bind
from CityOfBinds.src.BindFile.bindfile import BindFile
from CityOfBinds.src.BindGraphPublisher.node import BindFileNode
from CityOfBinds.src.BindGraphPublisher.graph import BindFileGraph
from CityOfBinds.src.BindGraphPublisher.publisher import BFGPublisher

class RotatingBind(BFGPublisher):
    def __init__(self, binds: list[Bind], is_circular: bool = True):
        super().__init__()
        self._binds = None
        self._trigger = None # TODO: 25-11-24 lookin into trigger mixin
        self.binds = binds
        self.is_circular = is_circular

    @property 
    def binds(self) -> list[Bind]:
        return self._binds

    @binds.setter
    def binds(self, binds: list[Bind]):
        self._binds = binds

    @property
    def trigger(self) -> str:
        return self._trigger

    def add_bind(self, bind: Bind) -> 'RotatingBind':
        self.binds.append(bind)
        return self

    def remove_bind(self, bind: Bind) -> 'RotatingBind':
        self.binds.remove(bind)
        return self

    def pop_bind(self, index: int) -> Bind:
        return self.binds.pop(index)
    
    def _populate_graph_publisher(self, bfg: BindFileGraph):
        nodes = [BindFileNode(index, BindFile().add_bind(bind)) for index, bind in enumerate(self.binds)]
        bfg.chain_nodes(nodes, close_loop=self.is_circular)
