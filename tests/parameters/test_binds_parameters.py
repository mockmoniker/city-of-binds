class TestBindParameters:

    # ({valid trigger}, {expected trigger})
    test_init_should_set_trigger_given_valid_trigger_parameters = [
        ("T", "T"),
        ("t", "T"),
        ("SPACE", "SPACE"),
        ("space", "SPACE"),
        ("SHIFT+T", "SHIFT+T"),
        ("shift+t", "SHIFT+T"),
        ("SHIFT+SPACE", "SHIFT+SPACE"),
        ("shift+space", "SHIFT+SPACE"),
    ]

    # ({valid slash commands}, {expected slash commands})
    test_init_should_set_slash_commands_given_valid_slash_commands_parameters = [
        (["command"], ["command"]),
        (["command with spaces"], ["command with spaces"]),
        (["command", "command2"], ["command", "command2"]),
        (["command with spaces", "command2 with spaces"], ["command with spaces", "command2 with spaces"]),
    ]

    # ({invalid trigger}, {expected error message})
    test_init_should_raise_value_error_given_invalid_trigger_parameters = [
        ("", "Trigger cannot be empty"),
        ("trigger with space", "Trigger cannot contain spaces"),
    ]

    # ({invalid slash commands}, {expected error message})
    test_init_should_raise_value_error_given_invalid_slash_commands_parameters = [
        ([], "Slash Commands list cannot be empty"),
        ([""], "Slash Commands list cannot contain empty commands"),
        (["command", ""], "Slash Commands list cannot contain empty commands"),
        (["", "command"], "Slash Commands list cannot contain empty commands"),
        (["command", "", "command2"], "Slash Commands list cannot contain empty commands"),
    ]

    # re-use init test cases
    test_set_trigger_should_set_trigger_given_valid_trigger_parameters = test_init_should_set_trigger_given_valid_trigger_parameters

    # re-use init test cases
    test_set_slash_commands_should_set_slash_commands_given_valid_slash_commands_parameters = test_init_should_set_slash_commands_given_valid_slash_commands_parameters

    # re-use init test cases
    test_set_trigger_should_raise_value_error_given_invalid_trigger_parameters = test_init_should_raise_value_error_given_invalid_trigger_parameters

    # re-use init test cases
    test_set_slash_commands_should_raise_value_error_given_invalid_slash_commands_parameters = test_init_should_raise_value_error_given_invalid_slash_commands_parameters

    # ({valid trigger}, {valid slash commands}, {expected bind string})
    test_bind_string_should_return_correct_string_given_valid_input_parameters = [
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

class TestToggleBindParameters(TestBindParameters):

    # ({valid powers}, {expected powers})
    test_init_should_set_toggle_off_powers_given_valid_powers_parameters = [
        (["power"], ["power"]),
        #(["POWER"], ["power"]),
        (["power with spaces"], ["power with spaces"]),
        (["power", "power2"], ["power", "power2"]),
        (["power with spaces", "power2 with spaces"], ["power with spaces", "power2 with spaces"]),
    ]

    # re-use toggle_off test cases
    test_init_should_set_toggle_on_powers_given_valid_powers_parameters = test_init_should_set_toggle_off_powers_given_valid_powers_parameters

    # ({valid power}, {expected power})
    test_init_should_set_auto_power_given_valid_auto_power_parameters = [
        ("power", "power"),
        #("POWER", "power"),
        ("power with spaces", "power with spaces"),
        ("power with number 0", "power with number 0"),
    ]

    # ({invalid powers}, {expected error message})
    test_init_should_raise_value_error_given_invalid_toggle_off_powers_parameters = [
        ([], "Slash Commands list cannot be empty"),
        ([""], "Slash Commands list cannot contain empty commands"),
        (["command", ""], "Slash Commands list cannot contain empty commands"),
        (["", "command"], "Slash Commands list cannot contain empty commands"),
        (["command", "", "command2"], "Slash Commands list cannot contain empty commands"),
    ]

    # re-use toggle_off test cases
    test_init_should_raise_value_error_given_invalid_toggle_on_powers_parameters = test_init_should_raise_value_error_given_invalid_toggle_off_powers_parameters

    # ({invalid power}, {expected error message})
    test_init_should_raise_value_error_given_invalid_auto_power_parameters = [
        ("", "Slash Commands list cannot be empty")
    ]

    #re-use init test cases
    test_set_toggle_off_powers_should_set_toggle_off_powers_given_valid_powers_parameters = test_init_should_set_toggle_off_powers_given_valid_powers_parameters

    # re-use init test cases
    test_set_toggle_on_powers_should_set_toggle_on_powers_given_valid_powers_parameters = test_init_should_set_toggle_off_powers_given_valid_powers_parameters

    # re-use init test cases
    test_set_auto_power_should_set_auto_power_given_valid_auto_power_parameters = test_init_should_set_auto_power_given_valid_auto_power_parameters

class TestWASDBindParameters(TestToggleBindParameters):

    # ({valid trigger}, {expected trigger})
    test_init_should_set_trigger_given_valid_trigger_parameters = [
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

    # ({valid trigger}, {expected direction})
    test_init_should_set_direction_given_valid_trigger_parameters = [
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

    # re-use init test cases
    test_set_trigger_should_set_trigger_given_valid_trigger_parameters = test_init_should_set_trigger_given_valid_trigger_parameters

    # re-use init test cases
    test_set_trigger_should_set_direction_given_valid_trigger_parameters = test_init_should_set_direction_given_valid_trigger_parameters

    