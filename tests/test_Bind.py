import pytest
from CityOfBinds import Bind
from scenarios import Scenarios

bind_under_test = Bind

class TestValidBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_trigger_scenarios)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = bind_under_test(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_slash_commands_input, expected_slash_commands_output", Scenarios.valid_set_slash_commands_scenarios)
    def test_init_should_set_slash_commands_given_valid_slash_commands(self, valid_slash_commands_input, expected_slash_commands_output):
        bind = bind_under_test(trigger="w", slash_commands=valid_slash_commands_input)
        assert bind.slash_commands == expected_slash_commands_output

class TestInvalidBindInitialization:
    @pytest.mark.parametrize("invalid_trigger_input, expected_error_message", Scenarios.invalid_set_trigger_scenarios)
    def test_init_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = bind_under_test(trigger=invalid_trigger_input, slash_commands=["command"])

    @pytest.mark.parametrize("invalid_slash_commands_input, expected_error_message", Scenarios.invalid_set_slash_commands_scenarios)
    def test_init_should_raise_value_error_given_invalid_slash_commands(self, invalid_slash_commands_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = bind_under_test(trigger="w", slash_commands=invalid_slash_commands_input)

class TestValidBindSetters:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_trigger_scenarios)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = bind_under_test(trigger="w", slash_commands=["command"])
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_slash_commands_input, expected_slash_commands_output", Scenarios.valid_set_slash_commands_scenarios)
    def test_set_slash_commands_should_set_slash_commands_given_valid_slash_commands(self, valid_slash_commands_input, expected_slash_commands_output):
        bind = bind_under_test(trigger="x", slash_commands=["command"])
        bind.slash_commands = valid_slash_commands_input
        assert bind.slash_commands == expected_slash_commands_output

class TestInvalidBindSetters:
    @pytest.mark.parametrize("invalid_trigger_input, expected_error_message", Scenarios.invalid_set_trigger_scenarios)
    def test_set_trigger_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input, expected_error_message):
        bind = bind_under_test(trigger="w", slash_commands=["command"])
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind.trigger = invalid_trigger_input

    @pytest.mark.parametrize("invalid_slash_commands_input, expected_error_message", Scenarios.invalid_set_slash_commands_scenarios)
    def test_set_slash_commands_should_raise_value_error_given_invalid_slash_commands(self, invalid_slash_commands_input, expected_error_message):
        bind = bind_under_test(trigger="w", slash_commands=["command"])
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind.slash_commands = invalid_slash_commands_input

class TestBindStrings:
    @pytest.mark.parametrize("valid_trigger_input, valid_slash_commands_input, expected_bind_string_output", Scenarios.valid_bind_string_scenarios)
    def test_bind_string_should_return_correct_string_given_valid_input(self, valid_trigger_input, valid_slash_commands_input, expected_bind_string_output):
        bind = bind_under_test(trigger=valid_trigger_input, slash_commands=valid_slash_commands_input)
        assert bind.bind_string == expected_bind_string_output
    