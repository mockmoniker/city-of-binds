from pathlib import Path
from ..utils import _Comment
from ...configs.constants import FileExtensions
from ...game import Bind
from ....utils import StrPath


BindContent = Bind | _Comment


class BindFile:
    def __init__(self, content_list: list[BindContent] = None):
        """Initialize the bind file with optional content."""
        self._contents = []
        self.contents = content_list if content_list is not None else []

    ### Properties
    @property
    def contents(self) -> list[BindContent]:
        """Get the contents of the bind file."""
        return self._contents

    @contents.setter
    def contents(self, content_list: list[BindContent]):
        """Set the contents of the bind file."""
        if content_list is not None:
            self._throw_error_on_invalid_content_list(content_list)
        self._contents = content_list

    @property
    def binds(self) -> list[Bind]:
        """Get only the Bind instances from the contents."""
        return [content for content in self._contents if isinstance(content, Bind)]

    ### Methods
    def add_bind(self, bind: Bind) -> "BindFile":
        """Add a Bind to the bind file."""
        self._throw_error_on_invalid_content_type(expected_type=Bind, content=bind)
        self._contents.append(bind)
        return self

    def add_comment(self, comment: _Comment) -> "BindFile":
        """Add a Comment to the bind file."""
        self._throw_error_on_invalid_content_type(
            expected_type=_Comment, content=comment
        )
        self._contents.append(comment)
        return self

    def clear(self) -> "BindFile":
        """Clear all contents and return self for chaining."""
        self._contents.clear()
        return self

    def preview(self) -> str:
        """Return the contents of the bind file as a string."""
        return self._build_file_contents()

    def is_empty(self) -> bool:
        """Check if the bind file has any content."""
        return len(self._contents) == 0

    def write_to_file(self, file_path: StrPath):
        """Write contents to the specified file path."""
        file_path = Path(file_path)

        # Auto-add .txt extension if missing
        if not file_path.suffix:
            file_path = file_path.with_suffix(FileExtensions.BIND_FILE)
        elif file_path.suffix != FileExtensions.BIND_FILE:
            raise ValueError(
                f"File must have '{FileExtensions.BIND_FILE}' extension, got '{file_path.suffix}'"
            )

        # Validate before writing
        self.validate_binds()

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(self._build_file_contents())

    def write_to_directory(self, filename: str, directory: StrPath = ".") -> None:
        """Convenience method to write to a directory with filename."""
        directory = Path(directory)
        full_path = directory / filename
        self.write_to_file(full_path)

    def validate_binds(self):
        for bind in self.binds:
            bind._validate()

    ### Helpers
    def _build_file_contents(self) -> str:
        if self.is_empty():
            return ""
        return "\n".join(str(content) for content in self._contents)

    ### Error Checking/Validation
    def _throw_error_on_invalid_content_list(self, content_list: list[BindContent]):
        if not isinstance(content_list, list):
            raise TypeError("Contents must be a list of Bind or Comment instances")
        for content in content_list:
            if not isinstance(content, (Bind, _Comment)):
                raise TypeError(
                    "All items in contents must be instances of Bind or Comment"
                )

    def _throw_error_on_invalid_content_type(self, expected_type, content):
        if not isinstance(content, expected_type):
            raise TypeError(
                f"Expected content of type {expected_type.__name__}, got {type(content).__name__}"
            )

    def __repr__(self):
        """Optional: Represent the BindFile with its contents."""
        return f"BindFile(contents={self._contents})"
