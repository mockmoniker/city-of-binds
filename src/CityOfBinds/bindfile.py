from CityOfBinds.binds import Bind

class BindFile:
    def __init__(self, filename: str, comment_banner: str = "", binds: list[Bind] = []):
        """Initialize the bind file with a filename."""
        self._filename = filename
        self._comment_banner = comment_banner
        self._binds = binds

        self.filename = filename
        self.comment_banner = comment_banner
        self.binds = binds

    ### Properties
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, filename: str):
        self._throw_error_on_invalid_filename(filename)
        self._filename = filename

    @property
    def comment_banner(self) -> str:
        return self._comment_banner

    @comment_banner.setter
    def comment_banner(self, comment_banner: str):
        self._comment_banner = comment_banner

    @property
    def binds(self) -> list[Bind]:
        return self._binds
    
    @binds.setter
    def binds(self, binds: list[Bind]):
        self._throw_error_on_invalid_binds(binds)
        self._binds = binds

    def write_to_file(self, path: str = ""):
        """Write all the binds to the file."""
        with open(path + "/" + self.filename, 'w') as file:
            file.write(self._build_message_string())
            for bind in self._binds:
                file.write(bind.bind_string + "\n")

    def _build_message_string(self) -> str:
        """Helper function to build a message string from the binds."""
        if self.comment_banner:
            return f"#\n# {self.comment_banner}\n#\n"
        return ""

    ### Error Checking/Validation
    def _throw_error_on_invalid_filename(self, filename: str):
        if not filename:
            raise ValueError("Filename cannot be empty")
        if not filename.endswith(".txt"):
            raise ValueError("Filename must end with .txt")

    def _throw_error_on_invalid_binds(self, binds: list[Bind]):
        return 

    def __repr__(self):
        """Optional: Represent the BindFile with its filename and binds."""
        return f"BindFile(filename={self.filename}, binds={self.binds})"
