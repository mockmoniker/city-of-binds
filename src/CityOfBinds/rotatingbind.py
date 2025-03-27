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
        file_count = len(self._bind_list)
        index_width = len(str(file_count - 1))  # Calculate the number of digits in the highest index

        for file_index, bind in enumerate(self._bind_list):
            next_file_index = (file_index + 1) % file_count
            formatted_file_index = str(file_index).zfill(index_width)  # Format with leading zeroes
            formatted_next_file_index = str(next_file_index).zfill(index_width)  # Format next index

            bind.slash_commands += f"{BIND_LOAD_FILE} {path}{file_prefix}{formatted_next_file_index}.txt"
            bind_file = BindFile(filename=f"{file_prefix}{formatted_file_index}.txt", binds=[bind])
            bind_file.write_to_file(path=path)

    ### Error Checking/Validation
    def _throw_error_on_invalid_bind_list(self, bind_list: list[Bind]):
        if not bind_list:
            raise ValueError("Bind list cannot be empty")