class FileExtensions:
    BIND_FILE = ".txt"
    POP_MENU = ".mnu"


class GameConstants:
    MAX_BIND_LENGTH = 255  # TODO: validate and check if this is full bind length or just commands (2025/12/06)
    COMMANDS_DELIM = "$$"
    OPTIONAL_COMMAND_UNDERSCORE = "_"


class TriggerConstants:
    TRIGGER_MODIFIER_SEPARATOR = "+"
    VALID_MODIFIERS = {"SHIFT", "CTRL", "CONTROL", "ALT"}
