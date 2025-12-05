from .rotating_bind import RotatingBind
from .wasd_rotating_bind import WASDRotatingBind
from .generic_rotating_binds import _RandomOrder
from ...game import BindFile


class RandomBinds(RotatingBind, _RandomOrder):
    def __init__(
        self,
        random_factor: int = 10,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        RotatingBind.__init__(
            self, is_silent=is_silent, absolute_path_links=absolute_path_links
        )
        self.random_factor = random_factor

    def _build_bind_files(self) -> list[BindFile]:
        bind_files = super()._build_bind_files()
        extended_bind_files = bind_files * self.random_factor
        return extended_bind_files


class RandomWalk(WASDRotatingBind, _RandomOrder):
    def __init__(
        self,
        include_jump: bool = False,
        is_silent: bool = True,
        absolute_path_links: bool = False,
    ):
        WASDRotatingBind.__init__(
            self,
            include_jump=include_jump,
            is_silent=is_silent,
            absolute_path_links=absolute_path_links,
        )

    def _connect_bind_file_graph(self, bfg, bind_file_indexes):
        bfg.make_k_regular(bind_file_indexes, k=len(self.directions))
