from ....configs.valid_input import TRIGGER_MODIFIERS, TRIGGER_KEYS
from ....configs.constants import GameConstants


class _Trigger:

    VALID_TRIGGER_KEYS = TRIGGER_KEYS
    VALID_TRIGGER_MODIFIERS = TRIGGER_MODIFIERS

    ### Initialization
    def __init__(self, trigger_string: str):
        """Initialize the trigger with a key and optional modifier."""
        self._modifier = None
        self._key = None

        self._throw_error_if_invalid_trigger_string(trigger_string)
        trigger_string = self._normalize_trigger_string(trigger_string)
        modifier, key = self._get_trigger_parts(trigger_string)
        self.modifier = modifier
        self.key = key

    # region Trigger Properties
    @property
    def modifier(self) -> str:
        return self._modifier

    @modifier.setter
    def modifier(self, modifier: str):
        self._modifier = self._normalize_and_validate_modifier(modifier)

    @property
    def key(self) -> str:
        return self._key

    @key.setter
    def key(self, key: str):
        self._key = self._normalize_and_validate_key(key)

    # endregion

    # region Trigger Methods
    def has_modifier(self) -> bool:
        return bool(self._modifier)

    def clear_modifier(self):
        self._modifier = ""

    # endregion

    # region Helper Methods
    def _get_trigger_parts(self, trigger_string: str) -> tuple[str, str]:
        """Extract modifier and key from trigger string."""
        modifier = self._get_modifier_from_trigger_string(trigger_string)
        key = self._get_key_from_trigger_string(trigger_string)
        return modifier, key

    def _get_modifier_from_trigger_string(self, trigger_string: str) -> str:
        """Helper function to extract the modifier from a trigger string."""
        parts = trigger_string.split(GameConstants.TRIGGER_DELIM)
        return parts[0] if len(parts) == 2 else ""

    def _get_key_from_trigger_string(self, trigger_string: str) -> str:
        """Helper function to extract the key from a trigger string."""
        parts = trigger_string.split(GameConstants.TRIGGER_DELIM)
        return parts[-1]  # Last part is always the key

    def _normalize_and_validate_modifier(self, modifier: str) -> str:
        modifier = self._normalize_modifier(modifier)
        self._throw_error_if_invalid_modifier(modifier)
        return modifier

    def _normalize_and_validate_key(self, key: str) -> str:
        key = self._normalize_key(key)
        self._throw_error_if_invalid_key(key)
        return key

    def _normalize_trigger_string(self, trigger_string: str) -> str:
        return trigger_string.strip()

    def _normalize_modifier(self, modifier: str) -> str:
        return modifier.strip().upper() if modifier else ""

    def _normalize_key(self, key: str) -> str:
        return key.strip().upper()

    def _build_trigger_string(self) -> str:
        """Build the complete trigger string from parts."""
        if self._modifier:
            return f"{self._modifier}{GameConstants.TRIGGER_DELIM}{self._key}"
        return self._key

    # endregion

    # region Error Checking Methods
    def _throw_error_if_invalid_trigger_string(self, trigger_string: str):
        # TODO: write trigger string validation better (2025/12/07)
        trigger_parts = trigger_string.split(GameConstants.TRIGGER_DELIM)
        if len(trigger_parts) > 2:
            raise ValueError(
                f"Invalid trigger format '{trigger_string}'. Trigger format must follow [MODIFIER+]<KEY>."
            )
        if len(trigger_parts) == 2 and (not trigger_parts[0] or not trigger_parts[1]):
            raise ValueError(
                f"Invalid trigger format '{trigger_string}'. Trigger format must follow [MODIFIER+]<KEY>."
            )

    def _throw_error_if_invalid_key(self, key: str):
        if not key:
            raise ValueError("Trigger key cannot be empty.")
        if " " in key:
            raise ValueError(
                f"Invalid trigger key '{key}'. Trigger key cannot contain spaces."
            )
        if key not in self.VALID_TRIGGER_KEYS:
            self._throw_invalid_key_error(key)

    def _throw_invalid_key_error(self, key: str):
        raise ValueError(
            f"Unknown trigger key '{key}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger keys."
        )

    def _throw_error_if_invalid_modifier(self, modifier: str):
        if not modifier:
            return
        if " " in modifier:
            raise ValueError(
                f"Invalid trigger modifier '{modifier}'. Trigger modifier cannot contain spaces."
            )
        if modifier not in self.VALID_TRIGGER_MODIFIERS:
            raise ValueError(
                f"Unknown trigger modifier '{modifier}'. Please see https://homecoming.wiki/wiki/List_of_Key_Names for list of valid trigger modifiers."
            )

    # endregion

    # region Dunder Methods
    def __repr__(self):
        """Override the default representation."""
        if self.modifier:
            return f"{self.__class__.__name__}(key='{self.key}', modifier='{self.modifier}')"
        else:
            return f"{self.__class__.__name__}(key='{self.key}')"

    def __str__(self):
        """Override the default string representation."""
        return self._build_trigger_string()

    def __eq__(self, other):
        """Override the default equality operator."""
        if not isinstance(other, _Trigger):
            return False
        return str(self) == str(other)

    # endregion
