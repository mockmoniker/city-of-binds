import copy
import random
from abc import ABC, abstractmethod
from ...game import BindFile
from ...content_publisher import BFGPublisher
from ...content_managers import BindFileGraph
from ...content_managers import BindTemplate
from ...content_managers import (
    BindFileTemplate,
    AdvanceOnTriggerType,
)
from ....utils.types import StrPath


class _GenericRotatingBind(ABC):
    def __init__(self, is_silent: bool = True, absolute_path_links: bool = False):
        self.bind_file_template: BindFileTemplate = BindFileTemplate()
        self.bfg_publisher: BFGPublisher = BFGPublisher(
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
        trigger_conditions = self._get_trigger_conditions()
        bfg = self._create_bind_file_graph(indexed_bind_files, trigger_conditions)
        self.bfg_publisher.publish_files(bfg, directory, parent_folder_name)

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

    def _get_trigger_conditions(self) -> dict:
        conditions = {}
        if self.bind_file_template.include_triggers:
            conditions["on_triggers"] = self.bind_file_template.include_triggers
        if self.bind_file_template.exclude_triggers:
            conditions["not_on_triggers"] = self.bind_file_template.exclude_triggers
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
            bfg.add_bind_file(copy.deepcopy(bind_file))


class _LoopTopology:
    def _connect_bind_file_graph(
        self, bfg: BindFileGraph, bind_file_indexes: list[int], trigger_conditions: dict
    ):
        bfg.loop(bind_file_indexes, trigger_conditions=trigger_conditions)


class _RandomOrder:
    def _index_bind_files(self, bind_files: list[BindFile]):
        random.shuffle(bind_files)
