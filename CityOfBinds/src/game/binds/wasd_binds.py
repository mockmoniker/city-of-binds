from .bind import Bind
from ..utils import _WASDTrigger
from ..utils import _CommandGroup


class WASDBind(Bind):
    """
    A specialized Bind that automatically injects movement commands for WASD keys.

    WASDBind extends the base Bind class to automatically add movement commands
    (+forward, +left, +backward, +right, +up) when using WASD or SPACE keys.
    The movement command is always inserted first, followed by any user-provided commands.

    Supported Keys:
        - W: +forward
        - A: +left
        - S: +backward
        - D: +right
        - SPACE: +up

    Example:
        >>> wasd_bind = WASDBind("W", ["powexectoggleon super speed"])
        >>> str(wasd_bind)  # 'W "+forward$$powexectoggleon super speed"'

        >>> wasd_bind = WASDBind("SHIFT+A")
        >>> str(wasd_bind)  # 'SHIFT+A "+left"'
    """

    TRIGGER_TYPE = _WASDTrigger

    # region Override Methods
    def _build_bind_string(self) -> str:
        """
        Build the WASD bind string with automatic movement command injection.

        Overrides the base Bind method to automatically prepend the appropriate
        movement command based on the trigger key before any user commands.

        Returns:
            Complete bind string with movement command first, then user commands
        """
        # Get the movement command for this WASD key
        movement_command = _CommandGroup().add_movement(
            self._get_direction(self.trigger)
        )
        # Combine movement with user commands (movement comes first)
        commands_with_movement = movement_command + self.commands
        return self._build_bind_string_from_components(
            self.trigger, commands_with_movement
        )

    # endregion

    # region Helper Methods
    def _get_direction(self, trigger: _WASDTrigger) -> str:
        """
        Get the movement direction string for a WASD trigger key.

        Args:
            trigger: WASD trigger containing the key to map to movement

        Returns:
            Movement direction string (e.g., "forward", "left", "backward", "right", "up")
        """
        return _WASDTrigger.KEY_TO_DIRECTION_MAP[trigger.key]

    # endregion


class iWASDBind(WASDBind):
    """
    An inverted WASD bind that uses opposite movement directions.

    iWASDBind (inverted WASD) extends WASDBind to use inverted movement controls.
    This is useful for creating binds that move in the opposite direction of
    the key pressed, which can be useful for certain (whacky) gameplay scenarios.

    Inverted Mappings:
        - W: +backward (instead of +forward)
        - A: +right (instead of +left)
        - S: +forward (instead of +backward)
        - D: +left (instead of +right)
        - SPACE: +up (unchanged)

    Example:
        >>> inverted_bind = iWASDBind("W", ["say going backward!"])
        >>> str(inverted_bind)  # 'W "+backward$$say going backward!"'
    """

    # region Override Methods
    def _get_direction(self, trigger: _WASDTrigger) -> str:
        """
        Get the inverted movement direction string for a WASD trigger key.

        Overrides the parent method to return the opposite direction for
        inverted movement controls. SPACE (up) remains unchanged.

        Args:
            trigger: WASD trigger containing the key to map to inverted movement

        Returns:
            Inverted movement direction string
        """
        direction = super()._get_direction(trigger)
        # Map each direction to its opposite
        opposite_directions = {
            "forward": "backward",
            "backward": "forward",
            "left": "right",
            "right": "left",
            "up": "up",  # SPACE remains unchanged
        }
        return opposite_directions[direction]

    # endregion
