import pytest
from CityOfBinds import Bind

valid_trigger_scenarios = [
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
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", valid_trigger_scenarios)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = Bind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("invalid_trigger_input", invalid_triggers)
    def test_init_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input):
        with pytest.raises(ValueError):
            bind = Bind(trigger=invalid_trigger_input, slash_commands=["command"])

class TestBindSetters:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", valid_trigger_scenarios)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = Bind(trigger="x", slash_commands=["command"])
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("invalid_trigger_input", invalid_triggers)
    def test_set_trigger_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input):
        bind = Bind(trigger="x", slash_commands=["command"])
        with pytest.raises(ValueError):
            bind.trigger = invalid_trigger_input