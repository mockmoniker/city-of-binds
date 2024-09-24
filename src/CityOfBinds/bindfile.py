from bind import Bind

class BindFile:
    def __init__(self, filename: str = "bind.txt", comment_banner: str = ""):
        """Initialize the bind file with a filename."""
        self.filename = filename
        self.comment_banner = comment_banner
        self.binds = []

    def add_bind(self, bind: Bind):
        """Add a bind to the file."""
        self.binds.append(bind)

    def write_to_file(self):
        """Write all the binds to the file."""
        with open(self.filename, 'w') as file:
            file.write(f"#\n# {self.comment_banner}\n#")
            for bind in self.binds:
                file.write(bind.get_bind_string() + "\n")

    def __repr__(self):
        """Optional: Represent the BindFile with its filename and binds."""
        return f"BindFile(filename={self.filename}, binds={self.binds})"
