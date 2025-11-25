import math
from pathlib import Path
from typing import Union

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

    @property
    def base(self) -> int:
        return len(self._alphabet)

    # endregion

    # region Methods
    def get_index_string(self, index: int) -> str:
        """ Get the string representation of the given index. """
        if index < 0:
            raise IndexError("Index cannot be negative.")

        if index == 0:
            return self._alphabet[0]

        digits = []
        while index:
            index, remainder = divmod(index, self.base)
            digits.append(self._alphabet[remainder])
        
        digits.reverse()
        return ''.join(digits)

    # endregion

    # region Dunder Methods
    def __getitem__(self, index: int) -> str:
        return self.get_index_string(index)
        
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
    DEFAULT_MAX_FILES_PER_FOLDER = 256
    DEFAULT_PADDING_BEHAVIOR = True

    """ Generates a folder/file path based off maximum files and max files per folder."""
    def __init__(
        self, 
        file_count: int,
        parent_directory: Union[str, Path] = ".",
        max_files_per_folder: int = DEFAULT_MAX_FILES_PER_FOLDER,
        enable_padding: bool = DEFAULT_PADDING_BEHAVIOR,
        indexer: Indexer = None,
    ):
        self.file_count = file_count
        self.parent_directory = Path(parent_directory)
        self.max_files_per_folder = max_files_per_folder
        self.enable_padding = enable_padding
        self.indexer = indexer if indexer else Indexer()

    @property
    def _depth(self) -> int:
        return self._calculate_depth(self.file_count, self.max_files_per_folder)
    
    @property
    def folder_depth(self) -> int:
        """Public property to get the folder depth (excluding file level)."""
        return self._depth - 1
    
    @property
    def _width(self) -> int:
        #num_files = min(self.file_count, self.max_files_per_folder)
        #return self._calculate_width(num_files, self.indexer.base)
        max_index = min(self.file_count, self.max_files_per_folder) - 1
        return len(self.indexer[max_index])

    @property
    def _root_width(self) -> int:
        """Calculate the required width for the root folder based on total file count."""
        root_subtree_capacity = self.max_files_per_folder ** (self._depth - 1)
        num_root_folders = math.ceil(self.file_count / root_subtree_capacity)

        max_root_index = num_root_folders - 1
        return len(self.indexer[max_root_index])

    @property
    def max_path_length(self) -> int:
        """Public property to get the maximum length of the entire file path."""
        return len(str(self.get_path(self.file_count - 1)))

    @property
    def _padding_char(self) -> str:
        return self.indexer[0]

    def get_path(self, file_index: int) -> Path:
        """Generate the folder/file path for a specific file index."""
        if file_index < 0 or file_index >= self.file_count:
            raise IndexError(f"File index '{file_index}' out of range [0, {self.file_count-1}]")
        
        depth = self._depth
        width = self._width
        padding_char = self._padding_char

        path_parts = []
        remaining_index = file_index

        capacity = self.max_files_per_folder ** (depth - 1)

        for _ in range(depth):
            part_index, remaining_index = divmod(remaining_index, capacity)
            part_string = self.indexer[part_index]
            if self.enable_padding:
                part_string = part_string.rjust(width, padding_char)
            path_parts.append(part_string)
            capacity //= self.max_files_per_folder

        if depth > 1:
            path_parts[0] = path_parts[0][-self._root_width:]

        return self.parent_directory / Path(*path_parts)

    def _calculate_depth(self, file_count: int, max_files_per_folder: int) -> int:
        """Calculate how many levels of nesting are needed."""
        if file_count <= max_files_per_folder:
            return 1

        return math.ceil(math.log(file_count, max_files_per_folder))

    def __getitem__(self, file_index: int) -> Path:
        return self.get_path(file_index)