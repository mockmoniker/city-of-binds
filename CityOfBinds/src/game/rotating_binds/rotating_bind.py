from ....utils.types.str_path import StrPath
from .generic_rotating_binds import _GenericRotatingBind, _LoopTopology


class RotatingBind(_LoopTopology, _GenericRotatingBind):
    def __init__(self, is_silent: bool = True, absolute_path_links: bool = False):
        _GenericRotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
