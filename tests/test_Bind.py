import pytest
from CityOfBinds import Bind
from scenarios import Scenarios

invalid_triggers = [
    "",
    "trigger with space",
]

class TestValidBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_trigger_scenarios)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = Bind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_slash_command_input, expected_slash_command_output", Scenarios.valid_set_slash_commands_scenarios)
    def test_init_should_set_slash_command_given_valid_slash_command(self, valid_slash_command_input, expected_slash_command_output):
        bind = Bind(trigger="x", slash_commands=valid_slash_command_input)
        assert bind.slash_commands == expected_slash_command_output

class TestInvalidBindInitialization:
    @pytest.mark.parametrize("invalid_trigger_input", invalid_triggers)
    def test_init_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input):
        with pytest.raises(ValueError):
            bind = Bind(trigger=invalid_trigger_input, slash_commands=["command"])

class TestValidBindSetters:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_trigger_scenarios)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = Bind(trigger="x", slash_commands=["command"])
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

class TestInvalidBindSetters:
    @pytest.mark.parametrize("invalid_trigger_input", invalid_triggers)
    def test_set_trigger_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input):
        bind = Bind(trigger="x", slash_commands=["command"])
        with pytest.raises(ValueError):
            bind.trigger = invalid_trigger_input