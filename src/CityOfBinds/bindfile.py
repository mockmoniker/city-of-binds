from typing import Union
from CityOfBinds.binds import Bind
from CityOfBinds.comments import Comment

class BindFileConstants:
    EXTENSION = ".txt"

class BindFile:
    def __init__(self, filename: str, content_list: list[Union[Bind, Comment]] = None):
        """Initialize the bind file with a filename."""
        self._filename = None

        self.filename = filename
        self.contensts = content_list if content_list is not None else []

    ### Properties
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, filename: str):
        self._throw_error_on_invalid_filename(filename)
        self._filename = filename

    ### Methods
    def preview(self) -> str:
        """Return the contents of the bind file as a string."""
        return self._build_file_contents()

    def write_to_path(self, path: str = ""):
        """Write all the binds to the file after validation."""
        self.validate_contents()
        with open(path / self.filename + BindFileConstants.EXTENSION, 'w') as file:
            file.write(self._build_file_contents())

    def validate_contents(self):
        for content in self.contents:
            if not isinstance(content, (Bind, Comment)):
                raise ValueError("All contents must be instances of Bind or Comment")
            if isinstance(content, Bind):
                content.validate()

    ### Helpers
    def _build_file_contents(self) -> str:
        file_contents = ""
        for content in self.contents:
            if isinstance(content, Comment):
                file_contents += content.comment_string + "\n"
            elif isinstance(content, Bind):
                file_contents += content.bind_string + "\n"
        return file_contents.strip()

    ### Error Checking/Validation
    def _throw_error_on_invalid_filename(self, filename: str):
        if not filename:
            raise ValueError("Filename cannot be empty")
        if '.' in filename:
            raise ValueError("Filename should not contain an extension")

    def __repr__(self):
        """Optional: Represent the BindFile with its filename and contents."""
        return f"BindFile(filename={self.filename}, contents={self.contents})"
