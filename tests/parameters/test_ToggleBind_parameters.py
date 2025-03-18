from parameters.test_Bind_parameters import TestBindParameters

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