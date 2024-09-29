import pytest
from CityOfBinds import ToggleBind

valid_trigger_cases = [
    ("T", "T"),
    ("t", "T"),
    ("SPACE", "SPACE"),
    ("space", "SPACE"),
    ("SHIFT+T", "SHIFT+T"),
    ("shift+t", "SHIFT+T"),
    ("SHIFT+SPACE", "SHIFT+SPACE"),
    ("shift+space", "SHIFT+SPACE"),
]

invalid_triggers = [
    "",
    "trigger with space",
]

class TestBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", valid_trigger_cases)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = ToggleBind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output