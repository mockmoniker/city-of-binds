from parameters.test_ToggleBind_parameters import TestToggleBindParameters

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

    