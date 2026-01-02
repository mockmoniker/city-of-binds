from ...configs.constants import BFGConstants
from ...content_managers.graph.bind_file_graph import BindFileGraph
from ..bind_file.bind_file import BindFile
from .generic_rotating_binds import _RandomOrder
from .rotating_bind import RotatingBind
from .wasd_rotating_bind import WASDRotatingBind


class RandomBinds(RotatingBind, _RandomOrder):
    def __init__(
        self,
        random_factor: int = 10,
        is_silent: bool = True,
        absolute_path_links: bool = False,
        loop_delay: int = 0,
    ):
        RotatingBind.__init__(
            self,
            is_silent=is_silent,
            absolute_path_links=absolute_path_links,
            loop_delay=loop_delay,
        )
        _RandomOrder.__init__(self, random_factor=random_factor)


class RandomWalk(_RandomOrder, WASDRotatingBind):
    def __init__(
        self,
        include_jump: bool = False,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        WASDRotatingBind.__init__(
            self,
            include_jump=include_jump,
            is_silent=is_silent,
            absolute_path_links=absolute_path_links,
            loop_delay=0,
        )
        _RandomOrder.__init__(self, random_factor=1)

    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int], trigger_conditions: dict
    ):
        bfg.make_k_regular(
            bind_file_indexes,
            k=len(self.direction_keys),
            trigger_conditions=trigger_conditions,
        )
        self._set_wasd_trigger_conditions(bfg, bind_file_indexes)

    def _set_wasd_trigger_conditions(
        self, bfg: BindFileGraph, bind_file_indexes: list[int]
    ):
        for file_index in bind_file_indexes:
            edges = list(bfg.edges(file_index))

            for (source, target), trigger in zip(edges, self.direction_keys):
                bfg.edges[source, target][BFGConstants.EDGE_DATA_KEY] = {
                    BFGConstants.INCLUSIVE_KEY: [trigger]
                }
