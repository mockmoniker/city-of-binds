from .generic_rotating_binds import _GenericRotatingBind, _LoopTopology


class RotatingBind(_LoopTopology, _GenericRotatingBind):
    def __init__(
        self,
        is_silent: bool = True,
        absolute_path_links: bool = False,
        loop_delay: int = 0,
    ):
        _LoopTopology.__init__(self, loop_delay=loop_delay)
        _GenericRotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
