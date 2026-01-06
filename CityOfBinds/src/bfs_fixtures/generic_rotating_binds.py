import random
from abc import ABC, abstractmethod

from ...utils.types.str_path import StrPath
from ..configs.constants import BFGConstants
from ..core.content_managers.graph.bind_file_graph import BindFileGraph
from ..core.content_managers.templates.bind_file_template import (
    BindFileTemplate,
    RotationPolicy,
)
from ..core.content_managers.templates.bind_template import BindTemplate
from ..core.content_publisher.bfg_publisher import BFGPublisher
from ..core.game_content.bind_file.bind_file import BindFile


class _GenericRotatingBind(ABC):
    def __init__(self, is_silent: bool = True, absolute_path_links: bool = False):
        self.bind_file_template: BindFileTemplate = BindFileTemplate()
        self.bfg_publisher: BFGPublisher = BFGPublisher(
            is_silent=is_silent, use_absolute_paths=absolute_path_links
        )

    @abstractmethod
    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int]
    ):
        pass

    def publish_bind_files(
        self, parent_folder_name: str = "", directory: StrPath = "."
    ):
        bfg = self.get_bfg()
        self.bfg_publisher.publish_files(bfg, directory, parent_folder_name)

    # TODO: make this reuse logic w/ publish bind files method (2025/12/07)
    def archive_bind_files(
        self,
        parent_folder_name: str = "",
        archive_directory: StrPath = ".",
        archive_format: str = "zip",
    ):
        bfg = self.get_bfg()
        self.bfg_publisher.publish_to_archive(
            bfg, archive_directory, parent_folder_name, archive_format
        )

    def add_bind_template(
        self,
        bind_template: BindTemplate,
        advance_on_trigger: RotationPolicy = RotationPolicy.DEFAULT,
    ):
        self.bind_file_template.add_bind_template(bind_template, advance_on_trigger)
        return self

    def get_bfg(self) -> BindFileGraph:
        indexed_bind_files = self._create_indexed_bind_files()
        trigger_conditions = self._get_trigger_conditions()
        bfg = self._create_bind_file_graph(indexed_bind_files, trigger_conditions)
        return bfg

    def _build_bind_files(self) -> list[BindFile]:
        return self.bind_file_template.build_all()

    def _create_indexed_bind_files(self) -> list[BindFile]:
        bind_files = self._build_bind_files()
        self._index_bind_files(bind_files)
        return bind_files

    def _index_bind_files(self, bind_files: list[BindFile]):
        pass

    def _get_trigger_conditions(self) -> dict:
        conditions = {}
        if self.bind_file_template.include_triggers:
            conditions[BFGConstants.INCLUSIVE_KEY] = (
                self.bind_file_template.include_triggers
            )
        if self.bind_file_template.exclude_triggers:
            conditions[BFGConstants.EXCLUSIVE_KEY] = (
                self.bind_file_template.exclude_triggers
            )
        if self.bind_file_template.quick_triggers:
            conditions[BFGConstants.QUICK_TRIGGER_KEY] = (
                self.bind_file_template.quick_triggers
            )
        return conditions

    def _create_bind_file_graph(
        self, indexed_bind_files: list[BindFile], trigger_conditions: dict
    ) -> BindFileGraph:
        bfg = BindFileGraph()
        self._add_bind_files_to_graph(bfg, indexed_bind_files)
        self._connect_bind_file_graph(
            bfg, range(len(indexed_bind_files)), trigger_conditions
        )
        return bfg

    def _add_bind_files_to_graph(self, bfg: BindFileGraph, bind_files: list[BindFile]):
        for bind_file in bind_files:
            bfg.add_bind_file(bind_file)


# TODO: deprecate and just making this rotatingbind? (2026/01/02)
class _LoopTopology:
    def __init__(self, loop_delay: int = 0):
        self.loop_delay = loop_delay

    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int], trigger_conditions: dict
    ):
        bfg.loop(
            bind_file_indexes,
            trigger_conditions=trigger_conditions,
            delay=self.loop_delay,
        )


class _RandomOrder:
    def __init__(self, random_factor: int = 1):
        self.random_factor = random_factor

    def _index_bind_files(self, bind_files: list[BindFile]):
        bind_files.extend(bind_files * (self.random_factor - 1))
        random.shuffle(bind_files)
