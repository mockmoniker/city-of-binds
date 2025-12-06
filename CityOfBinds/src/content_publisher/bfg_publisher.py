from pathlib import Path
from ..game import Bind
from ..game import BindFile, BindFileConstants
from ...utils import StrPath
from ...utils import _FileGraphPublisher


class BFGPublisher(_FileGraphPublisher):
    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        self.is_silent = is_silent
        super().__init__(
            absolute_path_links=absolute_path_links, file_graph_key="bind_file"
        )

    def _link_file(
        self,
        source_bind_file: BindFile,
        target_bind_file: BindFile,
        source_file_path: StrPath,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        trigger_conditions = edge_data["trigger_conditions"]
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

        if "on_triggers" in trigger_conditions:
            return bind.trigger in trigger_conditions["on_triggers"]

        if "not_on_triggers" in trigger_conditions:
            return bind.trigger not in trigger_conditions["not_on_triggers"]

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

    def _update_target_bind_file(
        self, target_bind_file: BindFile, trigger_conditions: dict[str, list[str]]
    ):
        if (
            "quick_triggers" not in trigger_conditions
            or not trigger_conditions["quick_triggers"]
        ):
            return

        for bind in target_bind_file.binds:
            if bind.trigger in trigger_conditions["quick_triggers"]:
                bind.trigger_on_key_up = (
                    True  # TODO: implement this on bind (2025/12/01)
                )

    def _write_file(self, bind_file: BindFile, path: StrPath):
        bind_file.write_to_file(Path(path))
