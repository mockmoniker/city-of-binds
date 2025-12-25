from pathlib import Path

from ...utils.file_graph_publisher import _FileGraphPublisher
from ...utils.types.str_path import StrPath
from ..configs.constants import BFGConstants, FileExtensions
from ..game.bind_file.bind_file import BindFile
from ..game.binds.bind import Bind


class BFGPublisher(_FileGraphPublisher):
    """
    Publisher for Bind File Graph (BFG) systems with file linking and cross-referencing.

    BFGPublisher specializes in publishing collections of interconnected bind files that
    can reference and load each other through bind commands. It handles the complex task
    of linking bind files together with conditional trigger-based loading, silent/verbose
    file transitions, and key up press activation.

    The publisher processes bind file graphs where nodes contain BindFile objects and edges
    define linking conditions between files. It automatically injects "bind_load_file"
    commands into appropriate binds based on trigger conditions, enabling sophisticated
    bind file rotation and navigation systems.

    Key Features:
        - Conditional bind file linking based on trigger inclusion/exclusion
        - Silent vs verbose file loading modes
        - Key up press activation for quick triggers
        - Automatic file path resolution with proper extensions
        - Integration with file graph publishing infrastructure

    Publisher Behavior:
        - Source files get "bind_load_file" commands added to specified binds
        - Target files get key up press activation for designated quick triggers
        - Linking conditions control which binds receive loading commands
        - File paths automatically receive .txt extensions for game compatibility

    Attributes:
        is_silent: Controls whether file transitions use silent mode (no chat messages)

    Example:
        >>> publisher = BFGPublisher(is_silent=True)
        >>> # Publish a graph where combat.txt links to travel.txt on F1 press
        >>> graph = create_bind_file_graph()
        >>> publisher.publish(graph, "/path/to/output/")
    """

    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        """
        Initialize a new BFGPublisher with specified linking behavior.

        Creates a publisher configured for bind file graph processing with control over
        file loading verbosity and path resolution. The publisher integrates with the
        file graph publishing infrastructure while providing BFG-specific functionality.

        Args:
            is_silent: Whether to use silent file loading (True) or show chat messages (False)
                      Silent mode prevents "Loading bind file..." messages in game chat
            absolute_path_links: Whether to use absolute paths in bind_load_file commands
                               False uses relative paths for portability

        Example:
            >>> # Silent publisher with relative paths (default)
            >>> publisher = BFGPublisher()
            >>> # Verbose publisher with absolute paths
            >>> publisher = BFGPublisher(is_silent=False, absolute_path_links=True)

        Note:
            Silent mode is typically preferred to avoid cluttering game chat with
            file loading messages during bind file transitions.
        """
        self.is_silent = is_silent
        super().__init__(
            absolute_path_links=absolute_path_links,
            file_graph_key=BFGConstants.NODE_DATA_KEY,
        )

    # region File Linking Methods
    def _link_file(
        self,
        source_bind_file: BindFile,
        target_bind_file: BindFile,
        source_file_path: StrPath,
        target_file_path: StrPath,
        edge_data: dict,
    ):
        """Link two bind files by updating source with load commands and target with key up settings."""
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
        """Add bind_load_file commands to qualifying binds in source file."""
        for bind in source_bind_file.binds:
            if self._should_link_bind(bind, trigger_conditions):
                self._link_bind(bind, target_file_path)

    def _should_link_bind(
        self, bind: Bind, trigger_conditions: dict[str, list[str]]
    ) -> bool:
        """Check if bind qualifies for file linking based on inclusion/exclusion conditions."""
        if trigger_conditions is None:
            return True

        if BFGConstants.INCLUSIVE_KEY in trigger_conditions:
            return bind.trigger in trigger_conditions[BFGConstants.INCLUSIVE_KEY]

        if BFGConstants.EXCLUSIVE_KEY in trigger_conditions:
            return bind.trigger not in trigger_conditions[BFGConstants.EXCLUSIVE_KEY]

        return True

    def _link_bind(self, bind: Bind, target_file_path: StrPath):
        """Add silent or verbose bind_load_file command to bind."""
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
        """Enable key up press activation for specified quick triggers."""
        if (
            BFGConstants.QUICK_TRIGGER_KEY not in trigger_conditions
            or not trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]
        ):
            return

        for bind in target_bind_file.binds:
            if bind.trigger in trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]:
                bind.trigger_on_key_up = True

    # endregion

    # region File Output Methods
    def _write_file(self, bind_file: BindFile, path: StrPath):
        """Write bind file to disk."""
        bind_file.write_to_file(Path(path))

    # endregion
