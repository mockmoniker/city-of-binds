class WASDMaps:
    KEY_TO_DIRECTION_MAP = {
        "W": "forward",
        "A": "left",
        "S": "backward",
        "D": "right",
        "SPACE": "up",
        "X": "down",
    }


class MovementMaps:
    DIRECTION_TO_MOVEMENT_MAP = {
        "forward": "+forward",
        "left": "+left",
        "backward": "+backward",
        "right": "+right",
        "up": "+up",
        "down": "+down",
    }

    OPPOSITE_DIRECTION = {
        "forward": "backward",
        "backward": "forward",
        "left": "right",
        "right": "left",
        "up": "up",
        "down": "down",
    }
