import shutil
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Iterator, Protocol, TypeAlias

from .pathgenerator import PathGenerator
from .types.str_path import StrPath

PathFactoryConstructor: TypeAlias = Callable[[int, StrPath], "PathFactoryProtocol"]


class FileGraphDefaults:
    FILE_GRAPH_KEY = "file"
    PARENT_FOLDER = "file_graph"
    PUBLISH_DIRECTORY = "."
    ABSOLUTE_PATH_LINKS = False
    ARCHIVE_FORMAT = "zip"
    PATH_FACTORY = PathGenerator


class FileGraphProtocol(Protocol):
    def nodes(self) -> Iterator: ...
    def out_edges(self, node_id: int, data: bool = False) -> Iterator[tuple]: ...

    nodes: any


class PathFactoryProtocol(Protocol):
    def __getitem__(self, index: int) -> Path: ...


class _FileGraphPublisher(ABC):
    def __init__(
        self,
        path_factory: PathFactoryConstructor = FileGraphDefaults.PATH_FACTORY,
        absolute_path_links: bool = FileGraphDefaults.ABSOLUTE_PATH_LINKS,
        file_graph_key: str = FileGraphDefaults.FILE_GRAPH_KEY,
    ):
        self._Path_Factory = path_factory
        self.absolute_path_links = absolute_path_links
        self.file_graph_key = file_graph_key

    def publish_files(
        self,
        file_graph: FileGraphProtocol,
        directory: StrPath = FileGraphDefaults.PUBLISH_DIRECTORY,
        parent_folder: str = FileGraphDefaults.PARENT_FOLDER,
    ):
        node_to_index = self._create_node_to_index_map(file_graph)
        paths = self._create_paths(len(node_to_index), directory, parent_folder)
        self._link_files(file_graph, node_to_index, paths)
        self._write_files(file_graph, node_to_index, directory, paths)

    def publish_to_archive(
        self,
        file_graph: FileGraphProtocol,
        archive_directory: StrPath = FileGraphDefaults.PUBLISH_DIRECTORY,
        parent_folder: str = FileGraphDefaults.PARENT_FOLDER,
        archive_format: str = FileGraphDefaults.ARCHIVE_FORMAT,
    ):
        """Publish files to a temporary directory, then zip it up."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Publish files to temporary directory
            self.publish_files(file_graph, temp_dir, parent_folder)

            # Create zip file path (zip name matches parent folder)
            archive_path = Path(archive_directory) / f"{parent_folder}"
            archive_path.parent.mkdir(parents=True, exist_ok=True)

            # Create zip from the temp directory root (includes parent_folder structure)
            shutil.make_archive(str(archive_path), archive_format, temp_dir)

    def _create_node_to_index_map(self, file_graph: FileGraphProtocol) -> dict:
        node_to_index = {}
        for index, node_id in enumerate(file_graph.nodes()):
            node_to_index[node_id] = index
        return node_to_index

    def _create_paths(
        self, file_count: int, directory: StrPath, parent_folder: str
    ) -> PathFactoryProtocol:
        if self.absolute_path_links:
            # TODO: test this resolve function, see if needed in my scenario (2025/12/01)
            parent_folder = Path(directory).resolve() / parent_folder
        return self._Path_Factory(file_count, parent_folder)

    def _link_files(self, file_graph: FileGraphProtocol, node_to_index: dict, paths):
        for source_node_id in file_graph.nodes():
            source_file = file_graph.nodes[source_node_id][self.file_graph_key]
            source_file_path = node_to_index[source_node_id]

            for _, target_node_id, edge_data in file_graph.out_edges(
                source_node_id, data=True
            ):
                target_file = file_graph.nodes[target_node_id][self.file_graph_key]
                target_file_path = paths[node_to_index[target_node_id]]

                self._link_file(
                    source_file,
                    target_file,
                    source_file_path,
                    target_file_path,
                    edge_data,
                )

    def _write_files(
        self,
        file_graph: FileGraphProtocol,
        node_to_index: dict,
        directory: StrPath,
        paths,
    ):
        for node_id in file_graph.nodes():
            file = file_graph.nodes[node_id][self.file_graph_key]
            file_path = Path(directory) / paths[node_to_index[node_id]]
            self._write_file(file, file_path)

    @abstractmethod
    def _link_file(
        self,
        source_file,
        target_file,
        source_file_path: StrPath,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        pass

    @abstractmethod
    def _write_file(self, file, path: StrPath):
        pass
