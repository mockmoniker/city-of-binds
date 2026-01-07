from ...utils.types.str_path import StrPath
from ..core.content_managers.graph.bind_file_graph import BindFileGraph
from ..core.content_publisher.bfg_publisher import BFGPublisher
from ..core.game_content.bind_file.bind_file import BindFile


class BindFileSystem:
    def __init__(self, is_silent: bool = True, use_absolute_paths: bool = False):
        self._bfg = BindFileGraph()
        self.bfg_publisher = BFGPublisher(is_silent, use_absolute_paths)

    @property
    def bfg(self) -> BindFileGraph:
        return self._bfg

    # region Exposed Bind File Graph Methods

    def add_bind_file(
        self, bind_file: BindFile, file_path_override: str = None
    ) -> "BindFileSystem":
        """Add a copy of a BindFile as a new node in the graph."""
        self._bfg.add_bind_file(bind_file, file_path_override)
        return self

    def link(
        self,
        source_bind_file_index: int,
        target_bind_file_index: int,
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileSystem":
        """Create a directed link from source to target bind file."""
        self._bfg.link(
            source_bind_file_index, target_bind_file_index, trigger_conditions, delay
        )
        return self

    def chain(
        self,
        bind_file_indexes: list[int],
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileSystem":
        """Create a linear chain of bind files in sequence."""
        self._bfg.chain(bind_file_indexes, trigger_conditions, delay)
        return self

    def loop(
        self,
        bind_file_indexes: list[int],
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileSystem":
        """Create a circular loop connecting bind files in list order."""
        self._bfg.loop(bind_file_indexes, trigger_conditions, delay)
        return self

    def make_k_regular(
        self,
        bind_file_indexes: list[int],
        k: int,
        trigger_conditions: dict = None,
        delay: int = 0,
    ) -> "BindFileSystem":
        """Create a k-regular graph where each bind file connects to exactly k others."""
        self._bfg.make_k_regular(bind_file_indexes, k, trigger_conditions, delay)
        return self

    def add_delay(
        self, source_bind_file_index: int, target_bind_file_index: int, steps: int = 1
    ) -> "BindFileSystem":
        """Insert copies of source node between two connected nodes."""
        self._bfg.add_delay(source_bind_file_index, target_bind_file_index, steps)
        return self

    def get_trigger_conditions(
        self, source_bind_file_index: int, target_bind_file_index: int
    ) -> dict:
        """Get the trigger conditions for a specific edge."""
        return self._bfg.get_trigger_conditions(
            source_bind_file_index, target_bind_file_index
        )

    def get_outgoing_links(self, bind_file_index: int) -> list[int]:
        """Get all node indexes that this bind file links to."""
        return self._bfg.get_outgoing_links(bind_file_index)

    def get_incoming_links(self, bind_file_index: int) -> list[int]:
        """Get all node indexes that link to this bind file."""
        return self._bfg.get_incoming_links(bind_file_index)

    def get_bind_file(self, bind_file_index: int) -> BindFile:
        """Retrieve the BindFile object stored at a specific node."""
        return self._bfg.get_bind_file(bind_file_index)

    def extend(
        self, other_graph: "BindFileGraph", merge_on: list[tuple[int, int]] = None
    ) -> "BindFileSystem":
        """Extend this graph with nodes and edges from another graph."""
        self._bfg.extend(other_graph, merge_on)
        return self

    def add_backup_side_effect(
        self, node_index: int, backup_target: int | StrPath
    ) -> "BindFileSystem":
        """Add a side-effect that creates a backup when bind file is loaded."""
        self._bfg.add_backup_side_effect(node_index, backup_target)
        return self

    def add_restore_side_effect(
        self, node_index: int, restore_source: int | StrPath
    ) -> "BindFileSystem":
        """Add a side-effect that restores from a backup when bind file is loaded."""
        self._bfg.add_restore_side_effect(node_index, restore_source)
        return self

    # endregion

    def publish_bind_files(
        self, parent_folder_name: str = "", directory: StrPath = "."
    ):
        self.bfg_publisher.publish_files(self.bfg, directory, parent_folder_name)

    def archive_bind_files(
        self,
        archive_directory: StrPath = ".",
        parent_folder_name: str = "",
        archive_format: str = "zip",
    ):
        self.bfg_publisher.publish_to_archive(
            self.bfg,
            archive_directory,
            parent_folder_name,
            archive_format,
        )
