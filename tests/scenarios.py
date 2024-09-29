class Scenarios:

    valid_set_trigger_scenarios = [
        ("T", "T"),
        ("t", "T"),
        ("SPACE", "SPACE"),
        ("space", "SPACE"),
        ("SHIFT+T", "SHIFT+T"),
        ("shift+t", "SHIFT+T"),
        ("SHIFT+SPACE", "SHIFT+SPACE"),
        ("shift+space", "SHIFT+SPACE"),
    ]

    valid_set_wasd_trigger_scenarios = [
        ("w", "W"),
        ("a", "A"),
        ("s", "S"),
        ("d", "D"),
        ("space", "SPACE"),
        ("W", "W"),
        ("A", "A"),
        ("S", "S"),
        ("D", "D"),
        ("SPACE", "SPACE")
    ]

    valid_set_wasd_direction_scenarios = [
        ("w", "+forward"),
        ("a", "+left"),
        ("s", "+backward"),
        ("d", "+right"),
        ("space", "+up"),
        ("W", "+forward"),
        ("A", "+left"),
        ("S", "+backward"),
        ("D", "+right"),
        ("SPACE", "+up")
    ]

    valid_set_slash_commands_scenarios = [
        (["command"], ["command"]),
        (["command with spaces"], ["command with spaces"]),
        (["command", "command2"], ["command", "command2"]),
        (["command with spaces", "command2 with spaces"], ["command with spaces", "command2 with spaces"]),
    ]

    valid_set_powers_scenarios = [
        (["power"], ["power"]),
        (["power with spaces"], ["power with spaces"]),
        (["power", "power2"], ["power", "power2"]),
        (["power with spaces", "power2 with spaces"], ["power with spaces", "power2 with spaces"]),
    ]

    valid_set_auto_power_scenarios = [
        ("power", "power"),
        ("power with spaces", "power with spaces"),
    ]