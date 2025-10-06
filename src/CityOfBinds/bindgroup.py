from CityOfBinds.binds import Bind
from CityOfBinds.comments import CommentBanner

class BindGroup:
    def __init__(self, binds: list[Bind] = [], group_banner_text: str = ""):
        """Initialize the bind group with binds and a group banner."""
        self._binds = None
        self._group_banner = None

        self.binds = binds
        self.group_banner = group_banner_text

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
        self._throw_error_on_invalid_binds(binds)
        self._binds = binds

    def write_to_file(self, path: str = ""):
        """Write all the binds to the file."""
        with open(path / self.filename, 'w') as file:
            file.write(self._build_message_string())
            for bind in self._binds:
                file.write(bind.bind_string + "\n")

    def _build_message_string(self) -> str:
        """Helper function to build a message string from the binds."""
        if self.comment_banner:
            comment_banner_lines = [comment_banner_line.strip() for comment_banner_line in self.comment_banner.split('\n')]
            max_line_length = max(len(line) for line in comment_banner_lines)
            border = '-' * (max_line_length + 4)
            return f"#\n# {self.comment_banner}\n#\n"
        return ""

    ### Error Checking/Validation
    def _throw_error_on_invalid_filename(self, filename: str):
        if not filename:
            raise ValueError("Filename cannot be empty")
        if not filename.endswith(".txt"):
            raise ValueError(f"Invalid filename {filename}. Filename must end with .txt")

    def __repr__(self):
        """Optional: Represent the BindFile with its filename and binds."""
        return f"BindFile(filename={self.filename}, binds={self.binds})"
