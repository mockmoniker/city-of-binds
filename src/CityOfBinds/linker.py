from functools import cached_property

class Indexer:
    """ Converts numerical indices to string representations using a configurable alphabet. """
    DEFAULT_ALPHABET = "0123456789ABCDEF"

    def __init__(self, alphabet: str = DEFAULT_ALPHABET):
        self._alphabet = None
        self.alphabet = alphabet

    # region Properties
    @property
    def alphabet(self) -> str:
        return self._alphabet

    @alphabet.setter
    def alphabet(self, value: str):
        self._throw_error_if_invalid_alphabet(value)
        self._alphabet = value

    @cached_property
    def base(self) -> int:
        return len(self._alphabet)

    # endregion

    # region Methods
    def get_converted_string(self, index: int) -> str:
        """ Get the string representation of the given index. """
        if index < 0:
            raise IndexError("Index cannot be negative.")
        if index == 0:
            return self._alphabet[0]

        result = []
        current_index = index

        while current_index > 0:
            digit = current_index % self.base
            result.append(self._alphabet[digit])
            current_index //= self.base

        result.reverse()
        return ''.join(result)

    # end region

    # region Dunder Methods
    def __getitem__(self, index: int) -> str:
        return self.get_converted_string(index)
        

    # endregion

    # region Error Checking Methods

    def _throw_error_if_invalid_alphabet(self, alphabet: str):
        self._throw_error_if_empty_alphabet(alphabet)
        self._throw_error_if_non_unique_alphabet_characters(alphabet)

    def _throw_error_if_empty_alphabet(self, alphabet: str):
        if not alphabet:
            raise ValueError("Alphabet cannot be empty.")

    def _throw_error_if_non_unique_alphabet_characters(self, alphabet: str):
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet characters must be unique.")

    # endregion

class PathGenerator:
    DEFAULT_MAX_FILES_PER_FOLDER = 255

    """ Generates a folder/file path based off maximum files and max files per folder."""
    def __init__(self, file_count: int, max_files_per_folder: int = DEFAULT_MAX_FILES_PER_FOLDER, indexer: Indexer = None):
        self.file_count = file_count
        self.max_files_per_folder = max_files_per_folder
        self.indexer = indexer if indexer else Indexer()

    def generate_paths(self) -> list[str]:
        paths = []
        for file_index in range(self.file_count):
            folder_index = file_index // self.max_files_per_folder
            file_name_index = file_index % self.max_files_per_folder

            folder_name = self.indexer.get_padded(folder_index, width=2)
            file_name = self.indexer.get_padded(file_name_index, width=2)

            path = f"{folder_name}/{file_name}"
            paths.append(path)
        return paths