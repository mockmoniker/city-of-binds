from typing import Union
from pathlib import Path
from CityOfBinds.binds import Bind
from CityOfBinds.comments import Comment

class BindFileConstants:
    EXTENSION = ".txt"

class BindFile:
    def __init__(self, content_list: list[Union[Bind, Comment]] = None):
        """Initialize the bind file with optional content."""
        self._contents = []
        self.contents = content_list if content_list is not None else []

    ### Properties
    @property
    def contents(self) -> list[Union[Bind, Comment]]:
        """Get the contents of the bind file."""
        return self._contents
    
    @contents.setter
    def contents(self, content_list: list[Union[Bind, Comment]]):
        """Set the contents of the bind file."""
        if content_list is not None:
            self._throw_error_on_invalid_content_list(content_list)
        self._contents = content_list

    @property
    def binds(self) -> list[Bind]:
        """Get only the Bind instances from the contents."""
        return [content for content in self._contents if isinstance(content, Bind)]

    ### Methods
    def add_bind(self, bind: Bind) -> 'BindFile':
        """Add a Bind to the bind file."""
        self._throw_error_on_invalid_content_type(expected_type=Bind, content=bind)
        self._contents.append(bind)
        return self

    def add_comment(self, comment: Comment) -> 'BindFile':
        """Add a Comment to the bind file."""
        self._throw_error_on_invalid_content_type(expected_type=Comment, content=comment)
        self._contents.append(comment)
        return self

    def clear(self) -> 'BindFile':
        """Clear all contents and return self for chaining."""
        self._contents.clear()
        return self

    def preview(self) -> str:
        """Return the contents of the bind file as a string."""
        return self._build_file_contents()

    def is_empty(self) -> bool:
        """Check if the bind file has any content."""
        return len(self._contents) == 0

    def write_to_file(self, file_path: Union[str, Path]):
        """Write contents to the specified file path."""
        file_path = Path(file_path)
        
        # Auto-add .txt extension if missing
        if not file_path.suffix:
            file_path = file_path.with_suffix(BindFileConstants.EXTENSION)
        elif file_path.suffix != BindFileConstants.EXTENSION:
            raise ValueError(f"File must have {BindFileConstants.EXTENSION} extension, got {file_path.suffix}")
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Validate and write
        self.validate_binds()
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self._build_file_contents())

    def write_to_directory(self, filename: str, directory: Union[str, Path] = ".") -> None:
        """Convenience method to write to a directory with filename."""
        directory = Path(directory)
        full_path = directory / filename
        self.write_to_file(full_path)

    def validate_binds(self):
        for content in self._contents:
            if isinstance(content, Bind):
                content.validate()

    ### Helpers
    def _build_file_contents(self) -> str:
        if self.is_empty():
            return ""
        return "\n".join(str(content) for content in self._contents)

    ### Error Checking/Validation
    def _throw_error_on_invalid_content_list(self, content_list: list[Union[Bind, Comment]]):
        if not isinstance(content_list, list):
            raise TypeError("Contents must be a list of Bind or Comment instances")
        for content in content_list:
            if not isinstance(content, (Bind, Comment)):
                raise TypeError("All items in contents must be instances of Bind or Comment")
        
    def _throw_error_on_invalid_content_type(self, expected_type, content):
        if not isinstance(content, expected_type):
            raise TypeError(f"Expected content of type {expected_type.__name__}, got {type(content).__name__}")

    def __repr__(self):
        """Optional: Represent the BindFile with its contents."""
        return f"BindFile(contents={self._contents})"

class BindFilePathIndexer:
    def __init__(self, file_count: int, file_prefix: str = ''):
        self.file_count = file_count
        self.file_prefix = file_prefix
        self._path_index_lookup_table = {}

        self._build_path_index_lookup_table()

    def get_file_path(self, index: int) -> str:
        """Get the file path for the given index."""
        if index not in self._path_index_lookup_table:
            raise ValueError(f"Index {index} is out of range for file count {self.file_count}")
        formatted_index = self._path_index_lookup_table[index]
        return f"{self.file_prefix}{formatted_index}{BindFileConstants.EXTENSION}"

    def _build_path_index_lookup_table(self):
        self._path_index_lookup_table = {}
        index_width = len(str(self.file_count - 1))  # Calculate the number of digits in the highest index

        for file_index in range(self.file_count):
            formatted_file_index = str(file_index).zfill(index_width)  # Format with leading zeroes
            self._path_index_lookup_table[file_index] = formatted_file_index



class BindFileLinkerConstants:
    BIND_LOAD_FILE_COMMAND = "bindloadfile"
    BIND_LOAD_FILE_SILENT_COMMAND = "bindloadfilesilent"

class BindFileLinker:
    def __init__(
            self, 
            bind_file_list: list[BindFile],
            is_silent: bool = False, 
            is_circular: bool = True,
            excluded_trigger_strings: list[str] = None
            ):
        self._bind_file_list = None
        self._is_silent = None
        self._is_circular = None
        self._excluded_trigger_strings = None

        self.bind_file_list = bind_file_list if bind_file_list is not None else []
        self.is_silent = is_silent
        self.is_circular = is_circular
        self.excluded_trigger_strings = excluded_trigger_strings if excluded_trigger_strings is not None else []

    ### Properties
    @property
    def is_silent(self) -> bool:
        return self._is_silent

    @is_silent.setter
    def is_silent(self, is_silent: bool):
        self._is_silent = is_silent
        if is_silent:
            self._bind_load_file_command = BindFileLinkerConstants.BIND_LOAD_FILE_SILENT_COMMAND
        else:
            self._bind_load_file_command = BindFileLinkerConstants.BIND_LOAD_FILE_COMMAND

    ### Methods
    def link_bind_files(self, path: Union[str, Path] = '', file_prefix: str = ''):
        """Link the bind files together by adding bind load commands."""
        file_count = len(self.bind_file_list)
        for file_index, file in enumerate(self.bind_file_list):
            # Skip linking for the last file if not circular
            if not self._is_circular and file_index == file_count - 1:
                continue
            for bind in file.binds:
                if bind.trigger in self._excluded_trigger_strings:
                    continue
                next_file_index = (file_index + 1) % file_count
                next_file_path = f"{path}/{file_prefix}{next_file_index}{BindFileConstants.EXTENSION}"
                bind.add_slash_command(f'{self._bind_load_file_command} {next_file_path}')