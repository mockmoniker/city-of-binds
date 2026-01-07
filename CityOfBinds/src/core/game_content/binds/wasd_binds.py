from ...._configs.maps import MovementMaps, WASDMaps
from ..command_group.command_group import CommandGroup
from ..utils.triggers.wasd_trigger import _WASDTrigger
from .bind import Bind


class WASDBind(Bind):
    """
    A specialized Bind that automatically injects movement commands for WASD keys.

    WASDBind extends the base Bind class to automatically add movement commands
    (+forward, +left, +backward, +right, +up, +down) when using WASD or SPACE/X keys.
    The movement command is always inserted first, followed by any user-provided commands.

    Supported Keys:
        - W: +forward
        - A: +left
        - S: +backward
        - D: +right
        - SPACE: +up
        - X: +down

    Example:
        >>> wasd_bind = WASDBind("W", ["powexectoggleon super speed"])
        >>> str(wasd_bind)  # 'W "+forward$$powexectoggleon super speed"'

        >>> wasd_bind = WASDBind("SHIFT+A")
        >>> str(wasd_bind)  # 'SHIFT+A "+left"'
    """

    TRIGGER_TYPE = _WASDTrigger

    # region Override Methods
    def _build_bind_string(self) -> str:
        """Build WASD bind string with automatic movement command injection."""
        movement_command = CommandGroup().add_movement(
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
        """Get movement direction string for WASD trigger key."""
        return WASDMaps.KEY_TO_DIRECTION_MAP[trigger.key]

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
        """Get inverted movement direction string for WASD trigger key."""
        direction = super()._get_direction(trigger)
        return MovementMaps.OPPOSITE_DIRECTION[direction]

    # endregion
