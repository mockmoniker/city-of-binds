from .bind import Bind
from ..utils import _WASDTrigger
from ..utils.slash_commands import _CommandGroup


class WASDBind(Bind):
    TRIGGER_TYPE = _WASDTrigger

    # region Override Methods
    def _build_bind_string(self) -> str:
        """Helper function to build the WASD bind string."""
        movement_command = _CommandGroup().add_movement(
            self._get_direction(self.trigger)
        )
        commands_with_movement = movement_command + self.commands
        return self._build_bind_string_from_components(
            self.trigger, commands_with_movement
        )

    # endregion

    # region Helper Methods
    def _get_direction(self, trigger: _WASDTrigger) -> str:
        return _WASDTrigger.KEY_TO_DIRECTION_MAP[trigger.key]

    # endregion


class iWASDBind(WASDBind):
    # region Override Methods
    def _get_direction(self, trigger: _WASDTrigger) -> set:
        direction = super()._get_direction(trigger)
        opposite_directions = {
            "forward": "backward",
            "backward": "forward",
            "left": "right",
            "right": "left",
        }
        return opposite_directions[direction]

    # endregion
