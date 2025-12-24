from pathlib import Path

from ....utils.types.str_path import StrPath
from ...configs.constants import FileExtensions
from ..binds.bind import Bind
from ..utils.comments.comment import _Comment

# Type alias for supported content types in bind files
BindContent = Bind | _Comment


class BindFile:
    """
    Represents a game bind file containing a collection of Binds and Comments.

    A BindFile manages an ordered collection of bind commands and comments that can be
    written to .txt files for use in City of Heroes/Villains. It provides methods for
    content manipulation, validation, file I/O, and preview generation.

    The BindFile maintains the order of its contents, allowing for precise control over
    how binds and comments appear in the generated file output.

    Example:
        >>> bf = BindFile()
        >>> bf.add_bind(Bind("F1", ["say hello"]))
        >>> bf.add_comment(_Comment("Greeting binds"))
        >>> bf.write_to_file("my_binds.txt")

    Attributes:
        contents: Ordered list of Bind and Comment instances
    """

    def __init__(self, content_list: list[BindContent] = None):
        """
        Initialize a new BindFile with optional starting content.

        Args:
            content_list: Optional list of Bind and/or Comment instances to initialize with.
                         If None, creates an empty BindFile.

        Raises:
            TypeError: If content_list is not a list or contains invalid content types

        Example:
            >>> # Empty bind file
            >>> bf = BindFile()
            >>> # Pre-populated bind file
            >>> binds = [Bind("F1", ["say hello"]), Bind("F2", ["say goodbye"])]
            >>> bf = BindFile(binds)
        """
        self._contents = []
        self.contents = content_list if content_list is not None else []

    # region Properties
    @property
    def contents(self) -> list[BindContent]:
        """
        Get the ordered list of all content in the bind file.

        Returns:
            List containing all Bind and Comment instances in their current order

        Example:
            >>> bf = BindFile([Bind("F1", ["say hi"]), _Comment("test")])
            >>> len(bf.contents)  # 2
        """
        return self._contents

    @contents.setter
    def contents(self, content_list: list[BindContent]):
        """
        Set the contents of the bind file, replacing all existing content.

        Args:
            content_list: List of Bind and/or Comment instances

        Raises:
            TypeError: If content_list is not a list or contains invalid types

        Example:
            >>> bf = BindFile()
            >>> bf.contents = [Bind("F1", ["say hello"])]
        """
        if content_list is not None:
            self._throw_error_on_invalid_content_list(content_list)
        self._contents = content_list

    @property
    def binds(self) -> list[Bind]:
        """
        Get only the Bind instances from the contents, filtering out comments.

        Returns:
            List of Bind instances in their current order

        Example:
            >>> bf = BindFile([Bind("F1", ["say hi"]), _Comment("test"), Bind("F2", ["say bye"])])
            >>> len(bf.binds)  # 2 (comments filtered out)
        """
        return [content for content in self._contents if isinstance(content, Bind)]

    # endregion

    # region Content Management Methods
    def add_bind(self, bind: Bind) -> "BindFile":
        """
        Add a Bind instance to the end of the bind file contents.

        Args:
            bind: The Bind instance to add

        Returns:
            Self for method chaining

        Raises:
            TypeError: If bind is not a Bind instance

        Example:
            >>> bf = BindFile()
            >>> bf.add_bind(Bind("F1", ["say hello"])).add_bind(Bind("F2", ["say goodbye"]))
            >>> len(bf.contents)  # 2
        """
        self._throw_error_on_invalid_content_type(expected_type=Bind, content=bind)
        self._contents.append(bind)
        return self

    def add_comment(self, comment: _Comment) -> "BindFile":
        """
        Add a Comment instance to the end of the bind file contents.

        Args:
            comment: The Comment instance to add

        Returns:
            Self for method chaining

        Raises:
            TypeError: If comment is not a Comment instance

        Example:
            >>> bf = BindFile()
            >>> bf.add_comment(_Comment("This is a header")).add_bind(Bind("F1", ["say hi"]))
        """
        self._throw_error_on_invalid_content_type(
            expected_type=_Comment, content=comment
        )
        self._contents.append(comment)
        return self

    def clear(self) -> "BindFile":
        """
        Remove all contents from the bind file.

        Returns:
            Self for method chaining

        Example:
            >>> bf = BindFile([Bind("F1", ["say hello"])])
            >>> bf.clear()
            >>> bf.is_empty()  # True
        """
        self._contents.clear()
        return self

    # endregion

    # region Query and Preview Methods
    def preview(self) -> str:
        """
        Generate a preview of the bind file content as it would appear when written to disk.

        Returns:
            String representation of all contents joined with newlines.
            Empty string if the bind file has no content.

        Example:
            >>> bf = BindFile([Bind("F1", ["say hello"]), _Comment("test comment")])
            >>> print(bf.preview())
            # F1 "say hello"
            # # test comment #
        """
        return self._build_file_contents()

    def is_empty(self) -> bool:
        """
        Check if the bind file contains any content.

        Returns:
            True if the bind file has no Binds or Comments, False otherwise

        Example:
            >>> bf = BindFile()
            >>> bf.is_empty()  # True
            >>> bf.add_bind(Bind("F1", ["say hello"]))
            >>> bf.is_empty()  # False
        """
        return len(self._contents) == 0

    # endregion

    # region File I/O Methods
    def write_to_file(self, file_path: StrPath):
        """
        Write the bind file contents to a disk file.

        Automatically adds .txt extension if not present and validates that the
        extension is .txt. Creates parent directories as needed. Validates all
        binds before writing.

        Args:
            file_path: Path where the bind file should be written (string or Path)

        Raises:
            ValueError: If file extension is not .txt or binds fail validation
            IOError: If file cannot be written

        Example:
            >>> bf = BindFile([Bind("F1", ["say hello"])])
            >>> bf.write_to_file("my_binds.txt")
            >>> bf.write_to_file("my_binds")  # Auto-adds .txt extension
        """
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
        """
        Convenience method to write the bind file to a specific directory with a filename.

        Args:
            filename: Name of the file to create (extension will be auto-added if missing)
            directory: Directory path where the file should be created (defaults to current directory)

        Example:
            >>> bf = BindFile([Bind("F1", ["say hello"])])
            >>> bf.write_to_directory("my_binds", "/home/user/binds")
            >>> # Creates /home/user/binds/my_binds.txt
        """
        directory = Path(directory)
        full_path = directory / filename
        self.write_to_file(full_path)

    # endregion

    # region Validation Methods
    def validate_binds(self):
        """
        Validate all Bind instances in the bind file.

        Calls the validate() method on each Bind instance, which checks for
        common issues like empty binds or binds that exceed length limits.

        Raises:
            ValueError: If any bind fails validation

        Note:
            Comments are not validated as they have no validation requirements.

        Example:
            >>> bf = BindFile([Bind("F1", [])])  # Empty bind
            >>> bf.validate_binds()  # Raises ValueError
        """
        for bind in self.binds:
            bind.validate()

    # endregion

    # region Private Helper Methods
    def _build_file_contents(self) -> str:
        """
        Build the complete file contents as a string.

        Joins all content items with newlines to create the final file output.
        Each Bind and Comment's __str__ method is used for string representation.

        Returns:
            Complete file contents as a string, or empty string if no content

        Note:
            This is an internal method used by preview() and write operations.
        """
        if self.is_empty():
            return ""
        return "\n".join(str(content) for content in self._contents)

    # endregion

    # region Validation and Error Handling
    def _throw_error_on_invalid_content_list(self, content_list: list[BindContent]):
        """
        Validate that content_list is a proper list of valid content types.

        Args:
            content_list: List to validate

        Raises:
            TypeError: If content_list is not a list or contains invalid types
        """
        if not isinstance(content_list, list):
            raise TypeError("Contents must be a list of Bind or Comment instances")
        for content in content_list:
            if not isinstance(content, (Bind, _Comment)):
                raise TypeError(
                    "All items in contents must be instances of Bind or Comment"
                )

    def _throw_error_on_invalid_content_type(self, expected_type, content):
        """
        Validate that content is of the expected type.

        Args:
            expected_type: The expected class type (Bind or _Comment)
            content: The content instance to validate

        Raises:
            TypeError: If content is not of the expected type
        """
        if not isinstance(content, expected_type):
            raise TypeError(
                f"Expected content of type {expected_type.__name__}, got {type(content).__name__}"
            )

    # endregion

    # region Magic Methods
    def __repr__(self):
        """
        Return a developer-friendly string representation of the BindFile.

        Returns:
            String in the format: BindFile(contents=[...])

        Example:
            >>> bf = BindFile([Bind("F1", ["say hi"])])
            >>> repr(bf)  # "BindFile(contents=[Bind('F1', ['say hi'])])"
        """
        return f"BindFile(contents={self._contents})"

    # endregion
