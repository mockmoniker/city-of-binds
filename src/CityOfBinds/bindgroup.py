from CityOfBinds.binds import Bind
from CityOfBinds.comments import Comment, CommentBanner

class BindGroup:
    DEFAULT_ALIGNMENT = "center"
    DEFAULT_COMMENT_FORMAT = "line"
    VALID_COMMENT_FORMATS = ["banner", "line"]
    def __init__(
            self, 
            binds_list: list[Bind] = [], 
            group_comment_text: str = "", 
            group_comment_alignment: str = DEFAULT_ALIGNMENT, 
            group_comment_minimum_width: int = Comment.MINIMUM_COMMENT_WIDTH, 
            group_comment_border_style: str = CommentBanner.DEFAULT_BORDER_STYLE,
            group_comment_format: str = DEFAULT_COMMENT_FORMAT
        ):
        """Initialize the bind group with binds and a group comment."""
        self._binds = None
        self._group_comment = None

        self.binds = binds_list
        self.group_comment = group_comment_text

    ### Properties
    @property
    def group_banner(self) -> str:
        return self._group_banner.comment_banner_string

    @group_banner.setter
    def group_banner(self, group_banner: str):
        self._group_banner = CommentBanner(group_banner)

    @property
    def binds(self) -> list[Bind]:
        return self._binds
    
    @binds.setter
    def binds(self, binds: list[Bind]):
        self._binds = binds


    ### Error Checking/Validation