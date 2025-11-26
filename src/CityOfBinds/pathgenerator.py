import math
from pathlib import Path
from typing import Union
from functools import lru_cache, cache

class BaseConverter:
    """ Converts numerical indices to string representations using a configurable alphabet. """
    DEFAULT_ALPHABET = "0123456789ABCDEF"

    def __init__(self, alphabet: str = DEFAULT_ALPHABET):
        self._alphabet = None
        self.alphabet = alphabet
        self._cached_convert = lru_cache(maxsize=1024)(self._convert)

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

    # region Convert Methods
    def convert(self, number: int, to_alphabet: str = None) -> str:
        self._validate_input(number, to_alphabet)
        return self._cached_convert(number, to_alphabet or self._alphabet)

    def _convert(self, number: int, to_alphabet: str) -> str:
        """ Get the string representation of the given number. """
        if number == 0:
            return to_alphabet[0]

        digits = []
        while number:
            number, remainder = divmod(number, len(to_alphabet))
            digits.append(to_alphabet[remainder])
        digits.reverse()

        return ''.join(digits)

    # endregion

    # region Error Checking Methods
    def _validate_input(self, number: int, alphabet: str = None):
        self._throw_error_if_number_is_negative(number)
        if alphabet is not None:
            self._throw_error_if_invalid_alphabet(alphabet)

    def _throw_error_if_invalid_alphabet(self, alphabet: str):
        self._throw_error_if_empty_alphabet(alphabet)
        self._throw_error_if_non_unique_alphabet_characters(alphabet)

    def _throw_error_if_empty_alphabet(self, alphabet: str):
        if not alphabet:
            raise ValueError("Alphabet cannot be empty.")

    def _throw_error_if_non_unique_alphabet_characters(self, alphabet: str):
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet characters must be unique.")

    def _throw_error_if_number_is_negative(self, number: int):
        if number < 0:
            raise ValueError("Cannot convert negative numbers.")

    # endregion

    # region Dunder Methods
    def __getitem__(self, number: int) -> str:
        return self.convert(number)
        
    # endregion

class PathGenerator:
    DEFAULT_PARENT_DIRECTORY = "."
    DEFAULT_MAX_FILES_PER_FOLDER = 256
    DEFAULT_PADDING_BEHAVIOR = True

    """ Generates a folder/file path based off maximum files and max files per folder."""
    def __init__(
        self, 
        file_count: int,
        parent_directory: Union[str, Path] = DEFAULT_PARENT_DIRECTORY,
        max_files_per_folder: int = DEFAULT_MAX_FILES_PER_FOLDER,
        enable_padding: bool = DEFAULT_PADDING_BEHAVIOR,
        path_alphabet: str = None,
    ):
        self._file_count = file_count
        self._parent_directory = Path(parent_directory)
        self._max_files_per_folder = max_files_per_folder
        self._enable_padding = enable_padding
        self._base_converter = BaseConverter(path_alphabet) if path_alphabet else BaseConverter()
        self._cached_paths = {}

        # region Helper Properties to Precompute
        self._depth = None
        self._capacity = None
        self._depth_capacities = None
        self._part_width = None
        self._root_width = None
        self._calculate_helper_properties()
        self._padding_char = self._base_converter.alphabet[0]

        # endregion

    # region Properties
    @property
    def folder_depth(self) -> int:
        """Public property to get the folder depth (excluding file level)."""
        return self._depth - 1

    @property
    def max_path_length(self) -> int:
        """Public property to get the maximum length of the entire file path."""
        return len(str(self.get_path(self._file_count - 1)))
    
    # endregion

    # region Path Generation Methods
    def get_path(self, file_index: int) -> Path:
        """Generate the folder/file path for a specific file index."""
        self._throw_error_if_index_out_of_range(file_index)

        return self._get_full_path(file_index)

    @cache
    def _get_full_path(self, file_index: int) -> Path:
        return self._parent_directory / self._get_relative_path(file_index)

    def _get_relative_path(self, file_index: int) -> Path:
        path_parts = self._make_path_parts(file_index)
        self._pad_path_parts(path_parts)
        self._trim_root_path_part(path_parts)

        return Path(*path_parts)

    def _make_path_parts(self, file_index: int) -> list[str]:
        path_parts = []
        remaining_index = file_index

        for depth_capacity in self._depth_capacities:
            part_index, remaining_index = divmod(remaining_index, depth_capacity)
            path_parts.append(self._base_converter[part_index])

        return path_parts

    def _pad_path_parts(self, path_parts: list[str]):
        if self._enable_padding:
            for i in range(len(path_parts)):
                path_parts[i] = path_parts[i].rjust(self._part_width, self._padding_char)

    def _trim_root_path_part(self, path_parts: list[str]):
        if self._depth > 1:
            path_parts[0] = path_parts[0][-self._root_width:]

    # endregion

    # region Helper Calculation Methods
    def _calculate_helper_properties(self):
        self._depth = self._calculate_depth(self._file_count, self._max_files_per_folder)
        self._capacity = self._calculate_capacity(self._max_files_per_folder, self._depth)
        self._depth_capacities = self._calculate_depth_capacities(self._depth, self._capacity, self._max_files_per_folder)
        self._part_width = self._calculate_part_width(self._file_count, self._max_files_per_folder)
        self._root_width = self._calculate_root_width(self._file_count, self._capacity)

    def _calculate_depth(self, file_count: int, max_files_per_folder: int) -> int:
        """Calculate how many levels of nesting are needed."""
        if file_count <= max_files_per_folder:
            return 1
        return math.ceil(math.log(file_count, max_files_per_folder))

    def _calculate_capacity(self, max_files_per_folder: int, depth: int) -> int:
        """Calculate the total capacity of files given the depth and max files per folder."""
        return max_files_per_folder ** (depth - 1)

    def _calculate_depth_capacities(self, depth: int, full_path_capacity: int, max_files_per_folder: int) -> list[int]:
        """Calculate the capacities at each depth level."""
        depth_capacities = []
        capacity = full_path_capacity

        for _ in range(depth):
            depth_capacities.append(capacity)
            capacity //= max_files_per_folder

        return depth_capacities

    def _calculate_part_width(self, file_count: int, max_files_per_folder: int) -> int:
        max_index = min(file_count, max_files_per_folder) - 1
        return len(self._base_converter[max_index])

    def _calculate_root_width(self, file_count: int, capacity: int) -> int:
        num_root_folders = math.ceil(file_count / capacity)
        max_root_index = num_root_folders - 1
        return len(self._base_converter[max_root_index])

    # endregion

    # region Error Checking Methods
    def _throw_error_if_index_out_of_range(self, file_index: int):
        if file_index < 0 or file_index >= self._file_count:
            raise IndexError(f"File index '{file_index}' out of range [0, {self._file_count-1}]")

    # endregion

    # region Dunder Methods
    def __getitem__(self, file_index: int) -> Path:
        return self.get_path(file_index)

    # endregion
    