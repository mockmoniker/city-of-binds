# /CityOfBinds/__init__.py
from ._version import __author__, __email__, __version__
from .src.content_managers.graph.bind_file_graph import BindFileGraph
from .src.content_managers.templates.bind_file_template import (
    BindFileTemplate,
    RotationPolicy,
)
from .src.content_managers.templates.bind_template import BindTemplate, WASDBindTemplate
from .src.content_publisher.bfg_publisher import BFGPublisher
from .src.game.bind_file.bind_file import BindFile
from .src.game.bind_file.comments.comment import Comment
from .src.game.bind_file.comments.comment_banner import CommentBanner
from .src.game.binds.bind import Bind
from .src.game.binds.wasd_binds import WASDBind, iWASDBind
from .src.game.command_group.command_group import CommandGroup
from .src.game.macros.macro import Macro
from .src.game.macros.macro_image import MacroImage
from .src.game.macros.macro_slot import MacroSlot
from .src.game.rotating_binds.changeling_binds import (
    ChangelingRotatingBindWS,
    ChangelingRotatingPB,
)
from .src.game.rotating_binds.random_binds import RandomBinds, RandomWalk
from .src.game.rotating_binds.rotating_bind import RotatingBind
from .src.game.rotating_binds.wasd_rotating_bind import WASDRotatingBind

__all__ = [
    "Bind",
    "WASDBind",
    "iWASDBind",
    "CommandGroup",
    "Macro",
    "MacroImage",
    "MacroSlot",
    "BindFile",
    "Comment",
    "CommentBanner",
    "RotatingBind",
    "RandomBinds",
    "RandomWalk",
    "WASDRotatingBind",
    "BindTemplate",
    "WASDBindTemplate",
    "BindFileTemplate",
    "BindFileGraph",
    "BFGPublisher",
    "ChangelingRotatingBindWS",
    "ChangelingRotatingPB",
]
