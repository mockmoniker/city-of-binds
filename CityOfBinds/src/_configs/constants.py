class GameConstants:
    MAX_BIND_LENGTH = 255  # TODO: validate and check if this is full bind length or just commands (2025/12/06)
    COMMANDS_DELIM = "$$"
    OPTIONAL_COMMAND_UNDERSCORE = "_"
    TRIGGER_DELIM = "+"
    ENABLE_KEY_UP_PREFIX = "+"
    SLOTS_PER_TRAY = 10
    TRAY_COUNT = 9


class GameExecutionCommands:
    EXECUTE_COMMAND = "/"
    EXECUTE_BIND = "/bind"


class BindFileConstants:
    FILE_EXTENSION = ".txt"
    STUB_TRIGGER = "KANA"
    STUB_COMMAND = "nop"


class BFGConstants:
    NODE_DATA_KEY = "bind_file"
    EDGE_DATA_KEY = "load_conditions"
    EXCLUSIVE_LOADING_TRIGGERS_KEY = "only_on_triggers"
    NON_LOADING_TRIGGERS_KEY = "not_on_triggers"
    QUICK_TRIGGER_KEY = "quick_triggers"
    SIDE_EFFECTS_KEY = "side_effects"
    BACKUP_SIDE_EFFECT_COMMAND = "showbindallfile"
    RESTORE_SIDE_EFFECT_COMMAND = "bindloadfilesilent"
    FILE_PATH_OVERRIDE_KEY = "use_bind_file_path"


class ChangelingConstants:
    DARK_NOVA = "dark nova"
    BLACK_DWARF = "black dwarf"
    BRIGHT_NOVA = "bright nova"
    WHITE_DWARF = "white dwarf"
    BOLT = "bolt"
    BLAST = "blast"
    DETONATION = "detonation"
    STRIKE = "strike"
    SMITE = "smite"
    ANTAGONIZE = "antagonize"
    EMMANATION = "emmanation"
    DRAIN = "drain"
    MIRE = "mire"
    SCATTER = "scatter"
    FLARE = "flare"
    SUBLIMATION = "sublimation"


class MacroCommands:
    MACRO = "macro"
    MACRO_SLOT = "macroslot"
    MACRO_IMAGE = "macroimage"


class SafeInstallValues:
    INSTALL_FILE_NAME = "_install.txt"
    LOAD_FILE_NAME = "_load.txt"
    UNLOAD_FILE_NAME = "_unload.txt"
    LOAD_MACRO_IMAGE = "InherentBase_Fury"
    UNLOAD_MACRO_IMAGE = "InherentBase_Anger"
    LOAD_MACRO_NAME = "Safe Load"
    UNLOAD_MACRO_NAME = "Safe Unload"


class Directions:
    FORWARD = "forward"
    LEFT = "left"
    BACKWARD = "backward"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
