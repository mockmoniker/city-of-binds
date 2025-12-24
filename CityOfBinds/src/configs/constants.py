class FileExtensions:
    BIND_FILE = ".txt"
    POP_MENU = ".mnu"


class GameConstants:
    MAX_BIND_LENGTH = 255  # TODO: validate and check if this is full bind length or just commands (2025/12/06)
    COMMANDS_DELIM = "$$"
    OPTIONAL_COMMAND_UNDERSCORE = "_"
    TRIGGER_DELIM = "+"
    ENABLE_KEY_UP_PREFIX = "+"


class BFGConstants:
    NODE_DATA_KEY = "bind_file"
    EDGE_DATA_KEY = "trigger_conditions"  # TODO: verify edge structure (2025/12/08)
    INCLUSIVE_KEY = "on_triggers"
    EXCLUSIVE_KEY = "not_on_triggers"
    QUICK_TRIGGER_KEY = "quick_triggers"
