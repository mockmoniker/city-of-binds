import copy
from .generic_rotating_binds import _GenericRotatingBind, _LoopTopology
from ...content_managers import WASDBindTemplate
from ...content_managers import AdvanceOnTriggerType


class WASDRotatingBind(_GenericRotatingBind, _LoopTopology):
    def __init__(
        self,
        include_jump: bool = False,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        _GenericRotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
        self.direction_keys = ["W", "A", "S", "D"]
        if include_jump:
            self.direction_keys.append("SPACE")
        self.wasd_bind_template = WASDBindTemplate(self.direction_keys[0])

    def _build_bind_files(self):
        self._append_wasd_binds()
        return super()._build_bind_files()

    def _append_wasd_binds(self):
        for direction in self.direction_keys:
            direction_template = copy.deepcopy(self.wasd_bind_template)
            direction_template.trigger = direction
            self.add_bind_template(direction_template, AdvanceOnTriggerType.INCLUDE)
