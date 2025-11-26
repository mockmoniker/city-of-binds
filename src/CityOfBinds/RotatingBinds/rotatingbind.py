from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile
from CityOfBinds.Graph.graph import BindFileNode, BindFileGraph, BFGPublisher

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
    
    def _populate_graph(self, bfg: BindFileGraph, nodes: list[BindFileNode]):
        for node_index in range(len(nodes) - 1):
            bfg.add_edge(nodes[node_index], nodes[node_index + 1])

        if self.is_circular:
            bfg.add_edge(nodes[-1], nodes[0])

    def _create_nodes(self) -> list[BindFileNode]:
        return [
            BindFileNode(
                id=index,
                bind_file=BindFile().add_bind(bind), 
            )
            for index, bind in enumerate(self.binds)
        ]