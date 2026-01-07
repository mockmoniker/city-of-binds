from ...core.content_managers.graph.bind_file_graph import BindFileGraph
from .generic_bfs_fixture import _GenericBFSFixture


class RotatingBind(_GenericBFSFixture):
    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
        loop_delay: int = 0,
    ):
        _GenericBFSFixture.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
        self.loop_delay = loop_delay

    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int], trigger_conditions: dict
    ):
        bfg.loop(
            bind_file_indexes,
            trigger_conditions=trigger_conditions,
            delay=self.loop_delay,
        )
