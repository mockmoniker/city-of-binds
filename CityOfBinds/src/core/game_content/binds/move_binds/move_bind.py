from ....._configs.constants import Directions
from ....._configs.defaults import DirectionKeys
from ...command_group.command_group import CommandGroup
from ...utils.triggers.trigger import _Trigger
from ..bind import Bind


class MoveBind(Bind):

    def __init__(
        self,
        trigger: str,
        commands: list[str] = None,
        forward_key: str = DirectionKeys.FORWARD_KEY,
        left_key: str = DirectionKeys.LEFT_KEY,
        backward_key: str = DirectionKeys.BACKWARD_KEY,
        right_key: str = DirectionKeys.RIGHT_KEY,
        jump_key: str = DirectionKeys.UP_KEY,
        down_key: str = DirectionKeys.DOWN_KEY,
    ):
        self.key_to_direction_map = {
            _Trigger(forward_key).key: Directions.FORWARD,
            _Trigger(left_key).key: Directions.LEFT,
            _Trigger(backward_key).key: Directions.BACKWARD,
            _Trigger(right_key).key: Directions.RIGHT,
            _Trigger(jump_key).key: Directions.UP,
            _Trigger(down_key).key: Directions.DOWN,
        }
        super().__init__(trigger, commands)

    # region Override Methods
    def _build_bind_string(self) -> str:
        """Build WASD bind string with automatic movement command injection."""
        movement_command = CommandGroup().add_movement(
            self.key_to_direction_map[self.trigger.key]
        )
        # Combine movement with user commands (movement comes first)
        commands_with_movement = movement_command + self.commands
        return self._build_bind_string_from_components(
            self.trigger, commands_with_movement
        )

    # endregion

    def _get_allowed_keys(self) -> list[str]:
        return list(self.key_to_direction_map.keys())
