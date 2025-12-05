from abc import ABC, abstractmethod
from typing import Protocol, Iterator, Callable
from pathlib import Path
from .pathgenerator import PathGenerator
from .types import StrPath


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
