import networkx as nx
import copy
from abc import ABC, abstractmethod
from pathlib import Path
from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile, BindFileConstants
from CityOfBinds.pathgenerator import PathGenerator

class BindFileNode:
    def __init__(self, id: int, bind_file: BindFile):
        self.id = id
        self.bind_file = bind_file

class BindFileGraph(nx.DiGraph):
    def __init__(self):
        super().__init__()

    def add_node(self, node: BindFileNode) -> 'BindFileGraph':
        super().add_node(node.id, bind_file=copy.deepcopy(node.bind_file))
        return self
    
    def add_edge(self, from_node: BindFileNode, to_node: BindFileNode, **condition) -> 'BindFileGraph':
        self.add_node(from_node)
        self.add_node(to_node)

        super().add_edge(from_node.id, to_node.id, **condition)
        return self

    def chain_nodes(self, node_list: list[BindFileNode], close_loop = False, **condition) -> 'BindFileGraph':
        for i in range(len(node_list) - 1):
            self.add_edge(node_list[i], node_list[i + 1], **condition)

        if close_loop and len(node_list) > 1:
            self.add_edge(node_list[-1], node_list[0], **condition)

        return self

    def subdivide_edge(self, from_node: BindFileNode, to_node: BindFileNode, new_node: BindFileNode, first_condition = None, second_condition = None) -> 'BindFileGraph':
        if not self.has_edge(from_node.id, to_node.id):
            raise ValueError(f"Edge from node {from_node.id} to node {to_node.id} does not exist.")

        self.remove_edge(from_node.id, to_node.id)
        self.add_node(new_node)
        super().add_edge(from_node.id, new_node.id, **(first_condition or {}))
        super().add_edge(new_node.id, to_node.id, **(second_condition or {}))

        return self

    def add_delay(self, from_node: BindFileNode, to_node: BindFileNode, steps: int = 1) -> 'BindFileGraph':
        for _ in range(steps):
            delay_node = BindFileNode(self.number_of_nodes(), from_node.bind_file)
            self.subdivide_edge(from_node, to_node, delay_node)
            from_node = delay_node
        return self

    def get_bind_file(self, node_id: int) -> BindFile:
        return self.nodes[node_id]['bind_file']

    def get_node_by_id(self, node_id: int) -> BindFileNode:
        return BindFileNode(node_id, self.get_bind_file(node_id))

class BFGPublisher(ABC):
    def __init__(self):
        """Initialize an empty directed graph."""
        self.is_silent = True

    def publish(self, directory: str = "."):
        """Write all bind files in the graph to the specified directory."""
        
        bfg = self._create_bind_file_graph()
        path_gen = PathGenerator(bfg.number_of_nodes(), parent_directory=directory)

        self._validate_graph_for_publishing(bfg)

        self._link_bind_files(bfg, path_gen)
        self._write_bind_files(bfg, path_gen)

    @abstractmethod
    def _populate_graph_publisher(self, bfg: BindFileGraph):
        pass

    def _create_bind_file_graph(self) -> BindFileGraph:
        bfg = BindFileGraph()

        self._populate_graph_publisher(bfg)
        self._throw_error_if_insufficient_nodes(len(bfg.nodes()))

        return bfg

    def _link_bind_files(self, bfg: BindFileGraph, path_gen: PathGenerator):
        """Link bind file contents based on graph structure and conditions."""

        for node_id in bfg.nodes():
            bind_file = bfg.get_bind_file(node_id)

            for _, target_node_id, edge_data in bfg.out_edges(node_id, data=True):
                on_condition = edge_data
                
                for bind in bind_file.binds:
                    if self._should_link_bind(bind, on_condition):
                        self._link_bind(bind, path_gen[target_node_id])

    def _should_link_bind(self, bind: Bind, condition: dict[str: any]) -> bool:
        # Placeholder for condition checking logic
        if condition is None:
            return True
        
        if 'on_triggers' in condition:
            return bind.trigger in condition['on_triggers']
        
        if 'not_on_triggers' in condition:
            return bind.trigger not in condition['not_on_triggers']
        
        return True

    def _link_bind(self, bind: Bind, next_file_path: Path):
        """Add a bind load command to the bind to load the next bind file."""
        if self.is_silent:
            bind.commands.add_bind_load_file_silent(next_file_path.with_suffix(BindFileConstants.EXTENSION))
        else:
            bind.commands.add_bind_load_file(next_file_path.with_suffix(BindFileConstants.EXTENSION))

    def _write_bind_files(self, bfg: BindFileGraph, path_gen: PathGenerator):
        """Write all bind files in the graph to disk."""
        for node_id in bfg.nodes():
            bind_file = bfg.get_bind_file(node_id)
            bind_file.write_to_file(path_gen[node_id])

    def _validate_graph_for_publishing(self, bfg: BindFileGraph):
        """Validate the graph structure before publishing."""
        # Placeholder for additional validation logic if needed
        pass

    def _throw_error_if_insufficient_nodes(self, node_count: int):
        if node_count < 2:
            raise ValueError(f"{self.__class__.__name__} requires at least two files be created. Got '{node_count}' files.")