import re

class Trigger:
    VALID_TRIGGER_MODIFIERS = [
        "",
        "SHIFT",
        "ALT",
        "CONTROL", "CTRL",
    ]
    VALID_TRIGGER_KEYS = [
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "ESC", "ESCAPE",
        "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
        "`", "TILDE",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "-", "MINUS",
        "EQUALS",
        "BACKSPACE",
        "TAB",
        "[", "LBRACKET",
        "]", "RBRACKET",
        "\\", "BACKSLASH",
        "CAPITAL",
        ";", "SEMICOLON",
        "'", "APOSTROPHE",
        "COMMA",
        ".", "PERIOD",
        "/", "SLASH",
        "SPACE",
        "APPS",
        "SYSRQ",
        "SCROLL",
        "PAUSE",
        "INSERT",
        "DELETE",
        "HOME",
        "END",
        "PAGEUP", "PRIOR",
        "PAGEDOWN", "NEXT",
        "UPARROW", "UP",
        "DOWNARROW", "DOWN",
        "LEFTARROW", "LEFT",
        "RIGHTARROW", "RIGHT",
        "LSHIFT",
        "RSHIFT",
        "LALT", "LMENU",
        "RALT", "RMENU",
        "LCONTROL", "LCTRL",
        "RCONTROL", "RCTRL",
        "RWIN",
        "LWIN",
        "NUMPAD0", "NUMPAD1", "NUMPAD2", "NUMPAD3", "NUMPAD4", "NUMPAD5", "NUMPAD6", "NUMPAD7", "NUMPAD8", "NUMPAD9",
        "NUMLOCK",
        "DIVIDE",
        "MULTIPLY",
        "SUBTRACT",
        "ADD",
        "DECIMAL",
        "NUMPADENTER"
        "KANJI",
        "CONVERT",
        "KANA",
        "LBUTTON", "LEFTCLICK", "LCLICK",
        "RBUTTON", "RIGHTCLICK", "RCLICK",
        "MBUTTON", "MIDDLECLICK", "MCLICK",
        "BUTTON4", "BUTTON5", "BUTTON6", "BUTTON7", "BUTTON8",
        "LEFTDOUBLECLICK", "LDOUBLECLICK",
        "RIGHTDOUBLECLICK", "RDOUBLECLICK",
        "MIDDLEDOUBLECLICK", "MDOUBLECLICK",
        "MOUSECHORD", "MOUSE_CHORD",
        "LEFTDRAGWORLD",
        "MIDDLEDRAG", "MDRAG"
        "MOUSEWHEEL",
        "WHEELPLUS", "MOUSEWHEEL_FORWARD",
        "WHEELMINUS", "MOUSEWHEEL_BACKWARD",
        "JOY1", "ABUTTON", "CROSSBUTTON",
        "JOY2", "BBUTTON", "CIRCLEBUTTON",
        "JOY3", "XBUTTON", "SQUAREBUTTON",
        "JOY4", "YBUTTON", "TRIANGLEBUTTON",
        "JOY5", "LEFTBUMPER", "LBUMPER", "LEFTSHOULDER", "LSHOULDER",
        "JOY6", "RIGHTBUMPER", "RBUMPER", "RIGHTSHOULDER", "RSHOULDER",
        "JOY7", "LEFTTRIGGER", "LTRIGGER",
        "JOY8", "RIGHTTRIGGER", "RTRIGGER",
        "JOY9", "LEFTTHUMB", "LTHUMB",
        "JOY10", "RIGHTTHUMB", "RTHUMB",
        "JOY11", "STARTBUTTON", "OPTIONSBUTTON",
        "JOY12", "BACKBUTTON", "SHAREBUTTON",
        "JOY13", "JOY14", "JOY15", "JOY16", "JOY17", "JOY18", "JOY19", "JOY20", "JOY21", "JOY22", "JOY23", "JOY24", "JOY25",
        "JOYPAD_UP", "DPADUP",
        "JOYPAD_DOWN", "DPADDOWN",
        "JOYPAD_LEFT", "DPADLEFT",
        "JOYPAD_RIGHT", "DPADRIGHT",
        "JOYSTICK1_UP",
        "JOYSTICK1_DOWN",
        "JOYSTICK1_LEFT",
        "JOYSTICK1_RIGHT",
        "JOYSTICK2_UP",
        "JOYSTICK2_DOWN",
        "JOYSTICK2_LEFT",
        "JOYSTICK2_RIGHT",
        "JOYSTICK3_UP",
        "JOYSTICK3_DOWN",
        "JOYSTICK3_LEFT",
        "JOYSTICK3_RIGHT",
        "POV1_UP",
        "POV1_DOWN",
        "POV1_LEFT",
        "POV1_RIGHT",
        "POV2_UP",
        "POV2_DOWN",
        "POV2_LEFT",
        "POV2_RIGHT",
        "POV3_UP",
        "POV3_DOWN",
        "POV3_LEFT",
        "POV3_RIGHT",
    ]

    ### Initialization
    def __init__(self, trigger_string: str):
        """Initialize the trigger with a key and optional modifier."""
        uppercase_trigger_string = trigger_string.upper()
        self._throw_error_on_invalid_trigger_string_format(uppercase_trigger_string)
        trigger_key, trigger_modifier = self._get_trigger_components_from_string(uppercase_trigger_string)

        self._trigger_key = trigger_key
        self._trigger_modifier = trigger_modifier

        self.trigger_key = trigger_key
        self.trigger_modifier = trigger_modifier

    ### Properties
    @property
    def trigger_key(self):
        return self._trigger_key
    
    @trigger_key.setter
    def trigger_key(self, trigger_key: str):
        trigger_key = trigger_key.upper()
        self._throw_error_on_invalid_trigger_key(trigger_key)
        self._trigger_key = trigger_key

    @property
    def trigger_modifier(self):
        return self._trigger_modifier

    @trigger_modifier.setter
    def trigger_modifier(self, trigger_modifier: str):
        trigger_modifier = trigger_modifier.upper()
        self._throw_error_on_invalid_trigger_modifier(trigger_modifier)
        self._trigger_modifier = trigger_modifier

    @property
    def trigger_string(self) -> str:
        return self._build_trigger_string()

    ### Methods
    def clear_modifier(self):
        self._trigger_modifier = ""

    ### Helpers
    def _build_trigger_string(self) -> str:
        """Build the trigger string from the key and modifier."""
        if self.trigger_modifier:
            return f"{self.trigger_modifier}+{self.trigger_key}"
        return self.trigger_key
    
    def _get_trigger_components_from_string(self, trigger_string: str) -> tuple[str, str]:
        """Helper function to split a trigger string into its key and modifier components."""
        trigger_components = trigger_string.split('+')
        if len(trigger_components) == 1:
            return trigger_components[0], ""
        elif len(trigger_components) == 2:
            return trigger_components[1], trigger_components[0]

    ### Error Checking/Validation
    def _throw_error_on_invalid_trigger_string_format(self, trigger_string: str):
        """Helper function to validate the overall trigger string format."""
        trigger_pattern = r"^(\w+\+)?\w+$" # pattern to match "[modifier+]<key>"
        if not re.match(trigger_pattern, trigger_string):
            raise ValueError(f"Invalid trigger format '{trigger_string}'. Format should be \"[modifier+]<key>\" where modifier is optional.")

    def _throw_error_on_invalid_trigger_key(self, trigger_key: str):
        if not trigger_key:
            raise ValueError("Invalid trigger key. Trigger key cannot be empty.")
        if ' ' in trigger_key:
            raise ValueError(f"Invalid trigger key '{trigger_key}'. Trigger key cannot contain spaces.")
        if trigger_key not in self.VALID_TRIGGER_KEYS:
            raise ValueError(f"Invalid trigger key '{trigger_key}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger keys.")
        
    def _throw_error_on_invalid_trigger_modifier(self, trigger_modifier: str):
        if ' ' in trigger_modifier:
            raise ValueError(f"Invalid trigger modifier '{trigger_modifier}'. Trigger modifier cannot contain spaces.")
        if trigger_modifier and trigger_modifier not in self.VALID_TRIGGER_MODIFIERS:
            raise ValueError(f"Invalid trigger modifier '{trigger_modifier}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger modifiers.")
        
    ### Overrides
    def __repr__(self):
        """Override the default representation."""
        return f"Trigger(trigger_key='{self.trigger_key}', trigger_modifier='{self.trigger_modifier}')"
    
    def __str__(self):
        """Override the default string representation."""
        return self.build_trigger_string()
    
    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, Trigger):
            return False
        return self.build_trigger_string() == other.build_trigger_string()
