from CityOfBinds.src.Binds.bind import Bind
from CityOfBinds.src.BindFile.bindfile import BindFile
from CityOfBinds.src.Triggers.trigger import Trigger
from CityOfBinds.src.BindFile.bindfiletemplate import BindFileTemplate
from CityOfBinds.src.BindGraphPublisher.node import BindFileNode
from CityOfBinds.src.BindGraphPublisher.graph import BindFileGraph
from CityOfBinds.src.BindGraphPublisher.publisher import BFGPublisher

class RotatingBind(BFGPublisher, BindFileTemplate):
    def __init__(self, trigger_advance_list: list[str] = None, is_circular: bool = True):
        BFGPublisher.__init__(self)
        BindFileTemplate.__init__(self)
        self.trigger_advance_list = [Trigger(trigger) for trigger in trigger_advance_list] if trigger_advance_list is not None else []
        self.is_circular = is_circular
    
    def _create_nodes(self) -> list[BindFileNode]:
        nodes = [BindFileNode(index, self.build()) for index in range(self.unique_count)]
        return nodes

    def _create_edges(self, bfg: BindFileGraph, nodes: list[BindFileNode]):
        bfg.chain_nodes(nodes, close_loop=self.is_circular, on_nodes=self.trigger_advance_list)