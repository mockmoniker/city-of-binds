import networkx as nx
from abc import ABC, abstractmethod
from pathlib import Path
from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile, BindFileConstants
from CityOfBinds.linker import PathGenerator

class BindFileNode:
    def __init__(self, node_id: int, bind_file: BindFile):
        self.node_id = node_id
        self.bind_file = bind_file

class BindFileGraph(nx.DiGraph):
    def __init__(self):
        super().__init__()

    def add_node(self, node: BindFileNode) -> 'BindFileGraph':
        super().add_node(node.node_id, bind_file=node.bind_file)
        return self
    
    def add_edge(self, from_node: BindFileNode, to_node: BindFileNode, **condition) -> 'BindFileGraph':
        self.add_node(from_node)
        self.add_node(to_node)

        super().add_edge(from_node.node_id, to_node.node_id, **condition)
        return self

    def get_bind_file(self, node_id: int) -> BindFile:
        return self.nodes[node_id]['bind_file']

class BFGPublisher(ABC):
    def __init__(self):
        """Initialize an empty directed graph."""
        self.is_silent = True

    def publish(self, directory: str = "."):
        """Write all bind files in the graph to the specified directory."""
        
        bfg = self._create_bind_file_graph()
        path_gen = PathGenerator(bfg.number_of_nodes(), parent_directory=directory)

        self._link_bind_files(bfg, path_gen)
        self._write_bind_files(bfg, path_gen)

    @abstractmethod
    def _populate_graph(self, bfg: BindFileGraph, nodes: list[BindFileNode]):
        pass

    @abstractmethod
    def _create_nodes(self) -> list[BindFileNode]:
        pass

    def _initialize_path_generator(self, bfg: BindFileGraph, directory: str = ".") -> PathGenerator:
        file_count = bfg.number_of_nodes()
        self._path_generator = PathGenerator(file_count=file_count, base=10, directory=directory)
        return self._path_generator

    def _create_bind_file_graph(self) -> BindFileGraph:
        bfg = BindFileGraph()

        nodes = self._create_nodes()

        self._throw_error_if_insufficient_nodes(len(nodes))

        self._populate_graph(bfg, nodes)

        return bfg

    def _link_bind_files(self, bfg: BindFileGraph, path_gen: PathGenerator):
        """Link bind file contents based on graph structure and conditions."""

        for node_id in bfg.nodes():
            bind_file = bfg.get_bind_file(node_id)

            # Get all outgoing edges from this node
            for _, target_node_id, edge_data in bfg.out_edges(node_id, data=True):
                condition = edge_data
                
                # Process each bind in the source bind file
                for bind in bind_file.binds:
                    if self._should_link_bind(bind, condition):
                        next_file_path = path_gen[target_node_id]
                        self._link_bind(bind, next_file_path)

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
        bind.commands.add_bind_load_file(next_file_path.with_suffix(BindFileConstants.EXTENSION), is_silent=self.is_silent)

    def _write_bind_files(self, bfg: BindFileGraph, path_gen: PathGenerator):
        """Write all bind files in the graph to disk."""
        for node_id in bfg.nodes():
            bind_file = bfg.get_bind_file(node_id)
            file_path = path_gen[node_id]
            bind_file.write_to_file(file_path)

    def _throw_error_if_insufficient_nodes(self, node_count: int):
        if node_count < 2:
            raise ValueError(f"{self.__class__.__name__} requires at least two files be created. Got '{node_count}' files.")