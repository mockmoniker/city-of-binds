from CityOfBinds.binds import Bind
from CityOfBinds.bindfile import BindFile

class RotatingBind():
    def __init__(self, bind_list: list[Bind]):
        self._bind_list = bind_list
        self.bind_list = bind_list

    ### Properties
    @property
    def bind_list(self) -> list[Bind]:
        return self._bind_list
    
    @bind_list.setter
    def bind_list(self, bind_list: list[Bind]):
        self._throw_error_on_invalid_bind_list(bind_list)
        self._bind_list = bind_list

    ### Methods
    def publish_bind_rotation_files(self, path: str = '', file_prefix: str = ''):
        """Write all the binds to the file."""
        for file_index, bind in enumerate(self._bind_list):
            next_file_index = (file_index + 1) % len(self._bind_list)
            bind.slash_commands += f"{BIND_LOAD_FILE} {path}{file_prefix}{next_file_index}.txt"
            bind_file = BindFile(filename=f"{file_prefix}{file_index}.txt", binds=[bind])
            bind_file.write_to_file(path=path)

    ### Error Checking/Validation
    def _throw_error_on_invalid_bind_list(self, bind_list: list[Bind]):
        if not bind_list:
            raise ValueError("Bind list cannot be empty")