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
        """
        Link two bind files by adding load commands and configuring target file properties.

        Processes a single edge in the bind file graph by updating both source and target
        files according to the edge's trigger conditions. The source file receives
        bind_load_file commands while the target file gets key up press configuration.

        Args:
            source_bind_file: The bind file that will load the target file
            target_bind_file: The bind file to be loaded by the source
            source_file_path: Path where the source file will be written
            target_file_path: Path where the target file will be written
            edge_data: Dictionary containing linking conditions and configuration

        Edge Data Structure:
            - Contains trigger conditions under BFGConstants.EDGE_DATA_KEY
            - May include inclusive/exclusive trigger lists
            - May specify quick triggers for key up press activation

        Example:
            >>> # Internal method called during graph processing
            >>> publisher._link_file(combat_file, travel_file, "combat", "travel", edge_data)
            >>> # combat_file now has bind_load_file commands for specified triggers

        Note:
            This method coordinates the two-phase linking process: source file updates
            for loading commands and target file updates for activation behavior.
        """
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
        """
        Add bind_load_file commands to qualifying binds in the source file.

        Iterates through all binds in the source file and adds file loading commands
        to those that meet the trigger conditions. This enables binds to transition
        to the target file when triggered.

        Args:
            source_bind_file: The file to modify with loading commands
            target_file_path: Path to the target file (will have .txt extension added)
            trigger_conditions: Dictionary specifying which triggers should link

        Trigger Condition Processing:
            - Checks each bind against inclusion/exclusion criteria
            - Only qualifying binds receive bind_load_file commands
            - Uses _should_link_bind() for condition evaluation

        Example:
            >>> # Add loading commands to F1 and F2 binds only
            >>> conditions = {"inclusive": ["F1", "F2"]}
            >>> publisher._update_source_bind_file(combat_file, "travel", conditions)
            >>> # F1 and F2 binds now load travel.txt when pressed

        Note:
            The actual command added depends on the is_silent setting:
            - Silent: bind_load_file_silent
            - Verbose: bind_load_file
        """
        for bind in source_bind_file.binds:
            if self._should_link_bind(bind, trigger_conditions):
                self._link_bind(bind, target_file_path)

    def _should_link_bind(
        self, bind: Bind, trigger_conditions: dict[str, list[str]]
    ) -> bool:
        """
        Determine whether a bind should receive file loading commands based on conditions.

        Evaluates trigger conditions to decide if the specified bind qualifies for
        file linking. Uses inclusion/exclusion logic to control which binds get
        bind_load_file commands added to their command sequences.

        Args:
            bind: The bind to evaluate for linking eligibility
            trigger_conditions: Dictionary containing condition specifications

        Returns:
            True if the bind should receive loading commands, False otherwise

        Condition Logic:
            - No conditions: All binds qualify (returns True)
            - Inclusive list: Only listed triggers qualify
            - Exclusive list: All triggers except listed ones qualify
            - Inclusive takes precedence over exclusive if both present

        Example:
            >>> conditions = {"inclusive": ["F1", "F2"]}
            >>> publisher._should_link_bind(f1_bind, conditions)  # True
            >>> publisher._should_link_bind(f3_bind, conditions)  # False
            >>>
            >>> conditions = {"exclusive": ["ESC"]}
            >>> publisher._should_link_bind(f1_bind, conditions)  # True
            >>> publisher._should_link_bind(esc_bind, conditions)  # False

        Note:
            This method implements the core filtering logic for selective file linking.
            The precedence order ensures predictable behavior when multiple conditions exist.
        """
        # No conditions specified - link all binds
        if trigger_conditions is None:
            return True

        # Inclusive list takes precedence - only listed triggers link
        if BFGConstants.INCLUSIVE_KEY in trigger_conditions:
            return bind.trigger in trigger_conditions[BFGConstants.INCLUSIVE_KEY]

        # Exclusive list - all triggers except listed ones link
        if BFGConstants.EXCLUSIVE_KEY in trigger_conditions:
            return bind.trigger not in trigger_conditions[BFGConstants.EXCLUSIVE_KEY]

        # Default behavior when conditions exist but no recognized keys
        return True

    def _link_bind(self, bind: Bind, target_file_path: StrPath):
        """
        Add the appropriate file loading command to a bind's command sequence.

        Appends either silent or verbose bind_load_file command to the bind based on
        the publisher's configuration. The command will load the target file when
        the bind is triggered, enabling file transitions.

        Args:
            bind: The bind to modify with a loading command
            target_file_path: Path to the target file (extension will be added)

        Command Types:
            - Silent mode: bind_load_file_silent (no chat notification)
            - Verbose mode: bind_load_file (shows loading message)

        Example:
            >>> # Silent mode
            >>> publisher._link_bind(f1_bind, "travel")
            >>> # F1 bind now includes: bind_load_file_silent travel.txt
            >>>
            >>> # Verbose mode
            >>> publisher.is_silent = False
            >>> publisher._link_bind(f2_bind, "combat")
            >>> # F2 bind now includes: bind_load_file combat.txt

        Note:
            The .txt extension is automatically added via FileExtensions.BIND_FILE.
            The command is appended to existing commands, not replaced.
        """
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
        """
        Configure key up press activation for quick triggers in the target file.

        Processes the target bind file to enable key up press activation for binds
        specified as quick triggers. This allows binds to activate on both key press
        and key release, providing more responsive control.

        Args:
            target_bind_file: The file to configure for key up press activation
            trigger_conditions: Dictionary containing quick trigger specifications

        Quick Trigger Processing:
            - Extracts quick trigger list from BFGConstants.QUICK_TRIGGER_KEY
            - Sets trigger_on_key_up = True for matching binds
            - Skips processing if no quick triggers specified

        Example:
            >>> # Configure F1 and F2 for key up press activation
            >>> conditions = {"quick_triggers": ["F1", "F2"]}
            >>> publisher._update_target_bind_file(travel_file, conditions)
            >>> # F1 and F2 binds now activate on both press and release

        Note:
            Key up press activation is typically used for movement or frequently
            accessed binds where immediate response on key release is desired.
        """
        # Skip if no quick triggers specified
        if (
            BFGConstants.QUICK_TRIGGER_KEY not in trigger_conditions
            or not trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]
        ):
            return

        # Enable key up press for specified quick triggers
        for bind in target_bind_file.binds:
            if bind.trigger in trigger_conditions[BFGConstants.QUICK_TRIGGER_KEY]:
                bind.trigger_on_key_up = True

    # endregion

    # region File Output Methods
    def _write_file(self, bind_file: BindFile, path: StrPath):
        """
        Write a bind file to disk at the specified path.

        Handles the physical file output by delegating to the BindFile's write_to_file
        method. This method serves as the final step in the publishing process,
        converting processed bind files into game-compatible text files.

        Args:
            bind_file: The processed bind file ready for output
            path: File system path where the bind file should be written

        Example:
            >>> # Internal method called during publishing
            >>> publisher._write_file(combat_file, "/output/combat.txt")
            >>> # File written to disk with all binds and commands

        Note:
            Path conversion to pathlib.Path is handled internally.
            The BindFile handles formatting and game compatibility requirements.
        """
        bind_file.write_to_file(Path(path))

    # endregion
