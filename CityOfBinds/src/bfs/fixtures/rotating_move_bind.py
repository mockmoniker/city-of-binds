import copy

from ...core.content_managers.templates.bind_file_template import RotationPolicy
from ...core.content_managers.templates.bind_template import BindTemplate
from ...core.content_managers.utils.commands_template import (
    _CommandsTemplate,  # TODO: implement base wasd bind to use commandstemplate (2025/12/27)
)
from ...core.game_content.binds.move_binds.wasd_bind import WASDBind
from .rotating_bind import RotatingBind


class RotatingMoveBind(RotatingBind):
    def __init__(
        self,
        include_jump: bool = False,
        is_silent: bool = True,
        absolute_path_links: bool = False,
        loop_delay: int = 0,
    ):
        RotatingBind.__init__(
            self,
            is_silent=is_silent,
            absolute_path_links=absolute_path_links,
            loop_delay=loop_delay,
        )
        self.direction_keys = ["W", "A", "S", "D"]
        if include_jump:
            self.direction_keys.append("SPACE")
        self.wasd_bind_template = BindTemplate(
            self.direction_keys[0], bind_type=WASDBind
        )

    def _build_bind_files(self):
        self._append_wasd_binds()
        return super()._build_bind_files()

    def _append_wasd_binds(self):
        for direction in self.direction_keys:
            direction_template = copy.deepcopy(self.wasd_bind_template)
            direction_template.trigger = direction
            self.add_bind_template(direction_template, RotationPolicy.ON_THIS_TRIGGER)
