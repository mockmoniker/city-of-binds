import random
import copy
from abc import ABC, abstractmethod
from pathlib import Path
from CityOfBinds.src.bind_file.bindfile import BindFile
from CityOfBinds.src.binds.bindtemplate import BindTemplate, WASDBindTemplate
from CityOfBinds.src.bind_file.bindfiletemplate import (
    BindFileTemplate,
    AdvanceOnTriggerType,
)
from CityOfBinds.src.bind_graph_publisher.graph import BindFileGraph
from CityOfBinds.src.bind_graph_publisher.publisher import BFGPublisher, BFGPublisher2

StrPath = str | Path


class _GenericRotatingBind(ABC):
    def __init__(self, is_silent: bool = True, absolute_path_links: bool = False):
        self.bind_file_template: BindFileTemplate = BindFileTemplate()
        self.bfg_publisher: BFGPublisher2 = BFGPublisher2(
            is_silent=is_silent, absolute_path_links=absolute_path_links
        )

    @abstractmethod
    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int]
    ):
        pass

    def publish_bind_files(
        self, parent_folder_name: str = "", directory: StrPath = "."
    ):
        indexed_bind_files = self._create_indexed_bind_files()
        bfg = self._create_bind_file_graph(indexed_bind_files)
        self.bfg_publisher.publish_files(
            indexed_bind_files, bfg, directory, parent_folder_name
        )

    def add_bind_template(
        self,
        bind_template: BindTemplate,
        advance_on_trigger: AdvanceOnTriggerType = AdvanceOnTriggerType.DEFAULT,
    ):
        self.bind_file_template.add_bind_template(bind_template, advance_on_trigger)
        return self

    def _build_bind_files(self) -> list[BindFile]:
        return self.bind_file_template.build_all()

    def _create_indexed_bind_files(self) -> list[BindFile]:
        bind_files = self._build_bind_files()
        self._index_bind_files(bind_files)
        return bind_files

    def _index_bind_files(self, bind_files: list[BindFile]):
        return bind_files

    def _create_bind_file_graph(
        self, indexed_bind_files: list[BindFile]
    ) -> BindFileGraph:
        bfg = BindFileGraph()
        self._add_bind_files_to_graph(bfg, indexed_bind_files)
        self._connect_bind_file_graph(bfg, range(len(indexed_bind_files)))
        return bfg

    def _add_bind_files_to_graph(self, bfg: BindFileGraph, bind_files: list[BindFile]):
        for bind_file in bind_files:
            bfg.add_bind_file(copy.deepcopy(bind_file))


class _RandomOrder:
    def _index_bind_files(self, bind_files: list[BindFile]):
        random.shuffle(bind_files)


class _LoopTopology:
    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int]
    ):
        bfg.loop(bind_file_indexes)


class RotatingBind(_LoopTopology, _GenericRotatingBind):
    def __init__(self, is_silent: bool = True, absolute_path_links: bool = False):
        _GenericRotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )


class RandomBind(RotatingBind, _RandomOrder):
    def __init__(
        self,
        random_factor: int = 10,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        RotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
        self.random_factor = random_factor

    def _build_bind_files(self) -> list[BindFile]:
        bind_files = super()._build_bind_files()
        extended_bind_files = bind_files * self.random_factor
        return extended_bind_files


class WASDRotatingBind(_GenericRotatingBind, _LoopTopology):
    def __init__(
        self,
        include_jump: bool = False,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        _GenericRotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
        self.directions = ["W", "A", "S", "D"]
        if include_jump:
            self.directions.append("SPACE")
        self.wasd_bind_template = WASDBindTemplate(self.directions[0])

    def _build_bind_files(self):
        self._append_wasd_binds()
        return super()._build_bind_files()

    def _append_wasd_binds(self):
        for direction in self.directions:
            direction_template = copy.deepcopy(self.wasd_bind_template)
            direction_template.trigger = direction
            self.add_bind_template(direction_template)


class RandomWalk(WASDRotatingBind, _RandomOrder):
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
        )

    def _connect_bind_file_graph(self, bfg, bind_file_indexes):
        bfg.make_k_regular(bind_file_indexes, k=len(self.directions))
