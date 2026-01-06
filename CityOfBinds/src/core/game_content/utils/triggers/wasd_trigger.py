from typing import Set

from ....._configs.maps import WASDMaps
from .trigger import _Trigger


class _WASDTrigger(_Trigger):
    VALID_TRIGGER_KEYS: Set[str] = set(WASDMaps.KEY_TO_DIRECTION_MAP.keys())

    # region Validation and Error Checking
    def _throw_invalid_key_error(self, key: str):
        raise ValueError(
            f"Unknown trigger key '{key}'. Valid WASD keys are: {', '.join(self.VALID_TRIGGER_KEYS)}"
        )

    # endregion
