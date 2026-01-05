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
    EDGE_DATA_KEY = "trigger_conditions"
    INCLUSIVE_KEY = "on_triggers"
    EXCLUSIVE_KEY = "not_on_triggers"
    QUICK_TRIGGER_KEY = "quick_triggers"
    SIDE_EFFECT_KEY = "side_effect"
    SIDE_EFFECT_TARGET_KEY = "side_effect_target"
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


class InstallFileNames:
    INSTALL_FILE_NAME = "_install.txt"
    LOAD_FILE_NAME = "_load.txt"
    UNLOAD_FILE_NAME = "_unload.txt"
