import tempfile
import shutil
from abc import ABC, abstractmethod
from typing import Type, Protocol, Callable, Iterator
from pathlib import Path
from CityOfBinds.src.binds.bind import Bind
from CityOfBinds.src.bind_file.bindfile import BindFile
from CityOfBinds.src.bind_file.constants import BindFileConstants
from CityOfBinds.src.bind_graph_publisher.node import BindFileNode
from CityOfBinds.src.bind_graph_publisher.graph import BindFileGraph
from CityOfBinds.utils.pathgenerator import PathGenerator

StrPath = str | Path


class FileGraphProtocol(Protocol):
    def out_edges(self, node_id: int, data: bool = False) -> Iterator[tuple]: ...


class PathFactoryProtocol(Protocol):
    def __getitem__(self, index: int) -> Path: ...


class _FileGraphPublisher(ABC):
    def __init__(
        self,
        path_factory: Callable[[int, StrPath], PathFactoryProtocol] = PathGenerator,
        absolute_path_links: bool = False,
    ):
        self._Path_Factory = path_factory
        self.absolute_path_links = absolute_path_links

    def publish_files(
        self,
        indexed_files: list,
        file_graph: FileGraphProtocol,
        directory: StrPath = ".",
        parent_folder: str = "",
    ):
        paths = self._create_paths(len(indexed_files), directory, parent_folder)
        self._link_files(indexed_files, file_graph, paths)
        self._write_files(indexed_files, directory, paths)

    def _create_paths(
        self, file_count: int, directory: StrPath, parent_folder: str
    ) -> PathFactoryProtocol:
        if self.absolute_path_links:
            # TODO: test this resolve function, see if needed in my scenario (2025/12/01)
            parent_folder = Path(directory).resolve() / parent_folder
        return self._Path_Factory(file_count, parent_folder)

    def _link_files(self, files: list, file_graph, paths):
        for file_index, source_file in enumerate(files):
            for _, target_index, edge_data in file_graph.out_edges(
                file_index, data=True
            ):
                target_file = files[target_index]
                self._link_file(
                    source_file, target_file, paths[target_index], edge_data
                )

    def _write_files(
        self,
        files: list,
        directory: StrPath,
        paths,
    ):
        for file_index, file in enumerate(files):
            file_path = paths[file_index]
            self._write_file(file, directory / file_path)

    @abstractmethod
    def _link_file(
        self, source_file, target_file, target_file_path: StrPath, edge_data: dict
    ):
        pass

    @abstractmethod
    def _write_file(self, file, path: StrPath):
        pass


class BFGPublisher2(_FileGraphPublisher):
    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        self.is_silent = is_silent
        super().__init__(absolute_path_links=absolute_path_links)

    def _link_file(
        self,
        source_bind_file: BindFile,
        target_bind_file: BindFile,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        self._update_source_bind_file(source_bind_file, target_file_path, edge_data)
        self._update_target_bind_file(target_bind_file, edge_data)

    def _update_source_bind_file(
        self,
        source_bind_file: BindFile,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        for bind in source_bind_file.binds:
            if self._should_link_bind(bind, edge_data):
                self._link_bind(bind, target_file_path)

    def _should_link_bind(self, bind: Bind, edge_data: dict[str:any]) -> bool:
        # Placeholder for condition checking logic
        if edge_data is None:
            return True

        if "on_triggers" in edge_data:
            return bind.trigger in edge_data["on_triggers"]

        if "not_on_triggers" in edge_data:
            return bind.trigger not in edge_data["not_on_triggers"]

        return True

    def _link_bind(self, bind: Bind, target_file_path: StrPath):
        if self.is_silent:
            bind.commands.add_bind_load_file_silent(
                Path(target_file_path).with_suffix(BindFileConstants.EXTENSION)
            )
        else:
            bind.commands.add_bind_load_file(
                Path(target_file_path).with_suffix(BindFileConstants.EXTENSION)
            )

    def _update_target_bind_file(self, target_bind_file: BindFile, edge_data: dict):
        if "key_up_triggers" not in edge_data or not edge_data["key_up_triggers"]:
            return

        for bind in target_bind_file.binds:
            if bind.trigger in edge_data["key_up_triggers"]:
                bind.trigger_on_key_up = (
                    True  # TODO: implement this on bind (2025/12/01)
                )

    def _write_file(self, bind_file: BindFile, path: StrPath):
        bind_file.write_to_file(Path(path))


class BFGPublisher(ABC):
    def __init__(self):
        """Initialize an empty directed graph."""
        self.is_silent = True

    def publish(
        self, parent_folder_name: str, directory: StrPath = "."
    ):  # TODO: check this directory/parent folder name nonsense (2025/11/30)
        """Write all bind files in the graph to the specified directory."""

        bfg = self._create_bind_file_graph()
        path_gen = PathGenerator(
            bfg.number_of_nodes(),
            parent_directory=Path(directory) / Path(parent_folder_name),
        )

        self._validate_graph_for_publishing(bfg)

        self._add_bind_links(bfg, path_gen)
        self._write_bind_files(bfg, path_gen)

    def publish_to_zip(self, parent_folder_name: str, zip_file_path: StrPath):
        """Publish bind files to a zip archive."""
        zip_file_path = Path(zip_file_path)

        with tempfile.TemporaryDirectory() as temp_dir:
            self.publish(parent_folder_name, temp_dir)
            shutil.make_archive(zip_file_path.with_suffix(""), "zip", temp_dir)

    @abstractmethod
    def _build_and_order_bind_files(self) -> list[BindFile]:
        pass

    @abstractmethod
    def _create_bind_file_links(self, bfg: BindFileGraph, bind_file_indexes: list[int]):
        pass

    def _create_bind_file_graph(self) -> BindFileGraph:
        bfg = BindFileGraph()
        self._add_initial_nodes(bfg)
        self._create_bind_file_links(bfg, list(bfg.nodes()))
        self._throw_error_if_insufficient_nodes(len(bfg.nodes()))

        return bfg

    def _add_initial_nodes(self, bfg: BindFileGraph):
        for bind_file in self._build_and_order_bind_files():
            bfg.add_bind_file(bind_file)

    def _add_bind_links(self, bfg: BindFileGraph, path_gen: PathGenerator):
        """Link bind file contents based on graph structure and conditions."""
        for node_id in bfg.nodes():
            bind_file = bfg.get_bind_file(node_id)

            for _, target_node_id, edge_data in bfg.out_edges(node_id, data=True):
                on_condition = edge_data

                for bind in bind_file.binds:
                    if self._should_link_bind(bind, on_condition):
                        self._link_bind(bind, path_gen[target_node_id])

    def _should_link_bind(self, bind: Bind, condition: dict[str:any]) -> bool:
        # Placeholder for condition checking logic
        if condition is None:
            return True

        if "on_triggers" in condition:
            return bind.trigger in condition["on_triggers"]

        if "not_on_triggers" in condition:
            return bind.trigger not in condition["not_on_triggers"]

        return True

    def _link_bind(self, bind: Bind, next_file_path: Path):
        """Add a bind load command to the bind to load the next bind file."""
        if self.is_silent:
            bind.commands.add_bind_load_file_silent(
                next_file_path.with_suffix(BindFileConstants.EXTENSION)
            )
        else:
            bind.commands.add_bind_load_file(
                next_file_path.with_suffix(BindFileConstants.EXTENSION)
            )

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
            raise ValueError(
                f"{self.__class__.__name__} requires at least two files be created. Got '{node_count}' files."
            )
