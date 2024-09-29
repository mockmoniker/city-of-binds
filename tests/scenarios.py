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

    valid_set_power_scenarios = [
        ("power", "power"),
        ("power with spaces", "power with spaces"),
    ]

    valid_bind_string_scenarios = [
        ("t", ["command"], "T \"command\""),
        ("t", ["command with spaces"], "T \"command with spaces\""),
        ("t", ["command", "command2"], "T \"command$$command2\""),
        ("t", ["command with spaces", "command2 with spaces"], "T \"command with spaces$$command2 with spaces\""),
        ("t", ["command", "command2", "command3"], "T \"command$$command2$$command3\""),
        ("t", ["command with spaces", "command2 with spaces", "command3 with spaces"], "T \"command with spaces$$command2 with spaces$$command3 with spaces\""),
        ("shift+t", ["command"], "SHIFT+T \"command\""),
        ("shift+t", ["command with spaces"], "SHIFT+T \"command with spaces\""),
        ("shift+t", ["command", "command2"], "SHIFT+T \"command$$command2\""),
        ("shift+t", ["command with spaces", "command2 with spaces"], "SHIFT+T \"command with spaces$$command2 with spaces\""),
        ("shift+t", ["command", "command2", "command3"], "SHIFT+T \"command$$command2$$command3\""),
        ("shift+t", ["command with spaces", "command2 with spaces", "command3 with spaces"], "SHIFT+T \"command with spaces$$command2 with spaces$$command3 with spaces\""),
    ]

    invalid_set_trigger_scenarios = [
        ("", "Trigger cannot be empty"),
        ("trigger with space", "Trigger cannot contain spaces"),
    ]

    invalid_set_slash_commands_scenarios = [
        ([], "Slash Commands list cannot be empty"),
        ([""], "Slash Commands list cannot contain empty commands"),
        (["command", ""], "Slash Commands list cannot contain empty commands"),
        (["", "command"], "Slash Commands list cannot contain empty commands"),
        (["command", "", "command2"], "Slash Commands list cannot contain empty commands"),
    ]

    invalid_set_powers_scenarios = [
        ([], "Slash Commands list cannot be empty"),
        ([""], "Slash Commands list cannot contain empty commands"),
        (["command", ""], "Slash Commands list cannot contain empty commands"),
        (["", "command"], "Slash Commands list cannot contain empty commands"),
        (["command", "", "command2"], "Slash Commands list cannot contain empty commands"),
    ]

    invalid_set_power_scenarios = [
        ("", "Slash Commands list cannot be empty")
    ]