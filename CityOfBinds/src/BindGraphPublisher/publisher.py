import tempfile
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from CityOfBinds.src.Binds.bind import Bind
from CityOfBinds.src.BindFile.constants import BindFileConstants
from CityOfBinds.src.BindGraphPublisher.node import BindFileNode
from CityOfBinds.src.BindGraphPublisher.graph import BindFileGraph
from CityOfBinds.utils.pathgenerator import PathGenerator

StrPath = str | Path

class BFGPublisher(ABC):
    def __init__(self):
        """Initialize an empty directed graph."""
        self.is_silent = True

    def publish(self, parent_folder_name: str, directory: StrPath = "."): # TODO: check this directory/parent folder name nonsense (2025/11/30) 
        """Write all bind files in the graph to the specified directory."""
        
        bfg = self._create_bind_file_graph()
        path_gen = PathGenerator(bfg.number_of_nodes(), parent_directory=Path(directory)/Path(parent_folder_name))

        self._validate_graph_for_publishing(bfg)

        self._link_bind_files(bfg, path_gen)
        self._write_bind_files(bfg, path_gen)

    def publish_to_zip(self, parent_folder_name: str, zip_file_path: StrPath):
        """Publish bind files to a zip archive."""
        zip_file_path = Path(zip_file_path)

        with tempfile.TemporaryDirectory() as temp_dir:
            self.publish(parent_folder_name, temp_dir)
            shutil.make_archive(zip_file_path.with_suffix(''), 'zip', temp_dir)

    @abstractmethod
    def _create_nodes(self) -> list[BindFileNode]:
        pass

    @abstractmethod
    def _create_edges(self, bfg: BindFileGraph, nodes: list[BindFileNode]):
        pass

    def _create_bind_file_graph(self) -> BindFileGraph:
        nodes = self._create_nodes()

        bfg = BindFileGraph()
        for node in nodes:
            bfg.add_node(node)

        self._create_edges(bfg, nodes)
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