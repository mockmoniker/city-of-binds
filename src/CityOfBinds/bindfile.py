from CityOfBinds.binds import Bind

class BindFile:
    def __init__(self, filename: str = "bind.txt", comment_banner: str = ""):
        """Initialize the bind file with a filename."""
        self.filename = filename
        self.comment_banner = comment_banner
        self.binds = []

    @property
    def binds(self) -> list[Bind]:
        """Return the binds."""
        return self._binds
    
    @binds.setter
    def binds(self, binds):
        """Set the binds."""
        self._throw_if_invalid_bind(binds)
        self._binds = binds

    def write_to_file(self):
        """Write all the binds to the file."""
        with open(self.filename, 'w') as file:
            file.write(f"#\n# {self.comment_banner}\n#")
            for bind in self._binds:
                file.write(bind.bind_string + "\n")

    def __repr__(self):
        """Optional: Represent the BindFile with its filename and binds."""
        return f"BindFile(filename={self.filename}, binds={self.binds})"
