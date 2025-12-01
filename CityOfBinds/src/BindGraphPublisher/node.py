from CityOfBinds.src.BindFile.bindfile import BindFile


class BindFileNode:
    def __init__(self, id: int, bind_file: BindFile):
        self.id = id
        self.bind_file = bind_file
