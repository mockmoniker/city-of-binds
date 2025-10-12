import re
from typing import Set

class Trigger:
    VALID_MODIFIERS: Set[str] = set([
        "SHIFT",
        "ALT",
        "CONTROL", "CTRL",
    ])
    VALID_KEYS: Set[str] = set([
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
        "NUMPADENTER",
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
        "MIDDLEDRAG", "MDRAG",
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
    ])

    ### Initialization
    def __init__(self, trigger_string: str):
        """Initialize the trigger with a key and optional modifier."""
        self._trigger_string = None
        self.trigger_string = trigger_string 

    ### Properties
    @property
    def trigger_string(self) -> str:
        return self._trigger_string

    @trigger_string.setter
    def trigger_string(self, trigger_string: str):
        formatted_trigger_string = trigger_string.upper()
        self._throw_error_on_invalid_trigger_string(trigger_string=formatted_trigger_string)
        self._trigger_string = formatted_trigger_string

    @property
    def key(self):
        return self._get_key_from_trigger_string(trigger_string=self.trigger_string)
    
    @key.setter
    def key(self, key: str):
        key = key.upper()
        self._throw_error_on_invalid_key(key)
        if self.modifier:
            self._trigger_string = f"{self.modifier}+{key}"
        else:
            self._trigger_string = key

    @property
    def modifier(self):
        return self._get_modifier_from_trigger_string(trigger_string=self.trigger_string)

    @modifier.setter
    def modifier(self, modifier: str):
        if modifier:
            formatted_modifier = modifier.upper()
            self._throw_error_on_invalid_modifier(formatted_modifier)
            self._trigger_string = f"{formatted_modifier}+{self.key}"
        else:
            self._trigger_string = self.key

    ### Methods
    def has_modifier(self) -> bool:
        return bool(self.modifier)

    def clear_modifier(self):
        self._trigger_string = self.key

    ### Helpers
    def _get_key_from_trigger_string(self, trigger_string: str) -> str:
        """Helper function to extract the key from a trigger string."""
        trigger_components = trigger_string.split('+')
        return trigger_components[-1]

    def _get_modifier_from_trigger_string(self, trigger_string: str) -> str:
        """Helper function to extract the modifier from a trigger string."""
        trigger_components = trigger_string.split('+')
        if len(trigger_components) == 2:
            return trigger_components[0]
        return ""

    ### Error Checking/Validation
    def _throw_error_on_invalid_trigger_string(self, trigger_string: str):
        """Helper function to validate the overall trigger string format."""
        self._throw_error_on_invalid_trigger_string_format(trigger_string)

        key = self._get_key_from_trigger_string(trigger_string)
        self._throw_error_on_invalid_key(key=key)

        modifier = self._get_modifier_from_trigger_string(trigger_string)
        self._throw_error_on_invalid_modifier(modifier=modifier)

    def _throw_error_on_invalid_trigger_string_format(self, trigger_string: str):
        """Helper function to validate the overall trigger string format."""
        trigger_pattern = r"^(\w+\+)?\w+$" # pattern to match "[modifier+]<key>"
        if not re.match(trigger_pattern, trigger_string):
            raise ValueError(f"Invalid trigger format '{trigger_string}'. Format should be \"[modifier+]<key>\" where modifier is optional.")

    def _throw_error_on_invalid_key(self, key: str):
        if not key:
            raise ValueError("Invalid trigger key. Trigger key cannot be empty.")
        if ' ' in key:
            raise ValueError(f"Invalid trigger key '{key}'. Trigger key cannot contain spaces.")
        if key not in self.VALID_KEYS:
            self._throw_invalid_key_error(key)

    def _throw_invalid_key_error(self, key: str):
        raise ValueError(f"Invalid trigger key '{key}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger keys.")

    def _throw_error_on_invalid_modifier(self, modifier: str):
        if ' ' in modifier:
            raise ValueError(f"Invalid trigger modifier '{modifier}'. Trigger modifier cannot contain spaces.")
        if modifier and modifier not in self.VALID_MODIFIERS:
            raise ValueError(f"Invalid trigger modifier '{modifier}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger modifiers.")
        
    ### Overrides
    def __repr__(self):
        """Override the default representation."""
        if self.modifier:
            return f"Trigger(key='{self.key}', modifier='{self.modifier}')"
        else:
            return f"Trigger(key='{self.key}')"

    def __str__(self):
        """Override the default string representation."""
        return self.trigger_string
    
    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, Trigger):
            return False
        return self.trigger_string == other.trigger_string

class WASDTrigger(Trigger):
    VALID_KEYS = ['W', 'A', 'S', 'D', 'SPACE']

    def _throw_invalid_key_error(self, key: str):
        raise ValueError(f"Invalid WASD trigger key '{key}'. Valid WASD keys are: {', '.join(self.VALID_KEYS)}")