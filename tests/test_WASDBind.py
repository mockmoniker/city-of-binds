import pytest
from CityOfBinds import WASDBind

valid_trigger_scenarioes = [
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

valid_trigger_direction_scenarios = [
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

invalid_triggers = [
    "",
    "trigger with space",
]

class TestBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", valid_trigger_scenarioes)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = WASDBind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_direciton", valid_trigger_direction_scenarios)
    def test_init_should_set_direction_given_valid_trigger(self, valid_trigger_input, expected_trigger_direciton):
        bind = WASDBind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind._direction == expected_trigger_direciton