from pathlib import Path

from ...utils.file_graph_publisher import _FileGraphPublisher
from ...utils.types.str_path import StrPath
from ..configs.constants import BFGConstants, FileExtensions
from ..game.bind_file.bind_file import BindFile
from ..game.binds.bind import Bind


class BFGPublisher(_FileGraphPublisher):
    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        self.is_silent = is_silent
        super().__init__(
            absolute_path_links=absolute_path_links,
            file_graph_key=BFGConstants.NODE_DATA_KEY,
        )

    def _link_file(
        self,
        source_bind_file: BindFile,
        target_bind_file: BindFile,
        source_file_path: StrPath,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        trigger_conditions = edge_data[BFGConstants.EDGE_DATA_KEY]
        self._update_source_bind_file(
            source_bind_file, target_file_path, trigger_conditions
        )
        self._update_target_bind_file(target_bind_file, trigger_conditions)

    def _update_source_bind_file(
        self,
        source_bind_file: BindFile,
        target_file_path: StrPath,
        trigger_conditions: dict[str, list[str]],
    ):
        for bind in source_bind_file.binds:
            if self._should_link_bind(bind, trigger_conditions):
                self._link_bind(bind, target_file_path)

    def _should_link_bind(
        self, bind: Bind, trigger_conditions: dict[str, list[str]]
    ) -> bool:
        # Placeholder for condition checking logic
        if trigger_conditions is None:
            return True

        if BFGConstants.INCLUSIVE_KEY in trigger_conditions:
            return bind.trigger in trigger_conditions[BFGConstants.INCLUSIVE_KEY]

        if BFGConstants.EXCLUSIVE_KEY in trigger_conditions:
            return bind.trigger not in trigger_conditions[BFGConstants.EXCLUSIVE_KEY]

        return True

    def _link_bind(self, bind: Bind, target_file_path: StrPath):
        if self.is_silent:
            bind.commands.add_bind_load_file_silent(
                Path(target_file_path).with_suffix(FileExtensions.BIND_FILE)
            )
        else:
            bind.commands.add_bind_load_file(
                Path(target_file_path).with_suffix(FileExtensions.BIND_FILE)
            )

    def _update_target_bind_file(
        self, target_bind_file: BindFile, trigger_conditions: dict[str, list[str]]
    ):
        if (
            BFGConstants.QUICK_TRIGGER_KEY not in trigger_conditions
            or not trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]
        ):
            return

        for bind in target_bind_file.binds:
            if bind.trigger in trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]:
                bind.trigger_on_key_up = True

    def _write_file(self, bind_file: BindFile, path: StrPath):
        bind_file.write_to_file(Path(path))
