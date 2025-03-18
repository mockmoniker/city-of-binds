import pytest
from CityOfBinds import Bind
from parameters.test_Bind_parameters import TestBindParameters

class TestValidBindInitializaiton:
    bind_under_test = Bind
    default_trigger = "t"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", TestBindParameters.test_init_should_set_trigger_given_valid_trigger_parameters)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = self.bind_under_test(trigger=valid_trigger_input, slash_commands=self.default_slash_commands)
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_slash_commands_input, expected_slash_commands_output", TestBindParameters.test_init_should_set_slash_commands_given_valid_slash_commands_parameters)
    def test_init_should_set_slash_commands_given_valid_slash_commands(self, valid_slash_commands_input, expected_slash_commands_output):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=valid_slash_commands_input)
        assert bind.slash_commands == expected_slash_commands_output

class TestInvalidBindInitialization:
    bind_under_test = Bind
    default_trigger = "t"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("invalid_trigger_input, expected_error_message", TestBindParameters.test_init_should_raise_value_error_given_invalid_trigger_parameters)
    def test_init_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = self.bind_under_test(trigger=invalid_trigger_input, slash_commands=self.default_slash_commands)

    @pytest.mark.parametrize("invalid_slash_commands_input, expected_error_message", TestBindParameters.test_init_should_raise_value_error_given_invalid_slash_commands_parameters)
    def test_init_should_raise_value_error_given_invalid_slash_commands(self, invalid_slash_commands_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=invalid_slash_commands_input)

class TestValidBindSetters:
    bind_under_test = Bind
    default_trigger = "t"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", TestBindParameters.test_set_trigger_should_set_trigger_given_valid_trigger_parameters)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_slash_commands_input, expected_slash_commands_output", TestBindParameters.test_set_slash_commands_should_set_slash_commands_given_valid_slash_commands_parameters)
    def test_set_slash_commands_should_set_slash_commands_given_valid_slash_commands(self, valid_slash_commands_input, expected_slash_commands_output):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        bind.slash_commands = valid_slash_commands_input
        assert bind.slash_commands == expected_slash_commands_output

class TestInvalidBindSetters:
    bind_under_test = Bind
    default_trigger = "t"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("invalid_trigger_input, expected_error_message", TestBindParameters.test_set_trigger_should_raise_value_error_given_invalid_trigger_parameters)
    def test_set_trigger_should_raise_value_error_given_invalid_trigger(self, invalid_trigger_input, expected_error_message):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind.trigger = invalid_trigger_input

    @pytest.mark.parametrize("invalid_slash_commands_input, expected_error_message", TestBindParameters.test_set_slash_commands_should_raise_value_error_given_invalid_slash_commands_parameters)
    def test_set_slash_commands_should_raise_value_error_given_invalid_slash_commands(self, invalid_slash_commands_input, expected_error_message):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind.slash_commands = invalid_slash_commands_input

class TestBindStrings:
    bind_under_test = Bind

    @pytest.mark.parametrize("valid_trigger_input, valid_slash_commands_input, expected_bind_string_output", TestBindParameters.test_bind_string_should_return_correct_string_given_valid_input_parameters)
    def test_bind_string_should_return_correct_string_given_valid_input(self, valid_trigger_input, valid_slash_commands_input, expected_bind_string_output):
        bind = self.bind_under_test(trigger=valid_trigger_input, slash_commands=valid_slash_commands_input)
        assert bind.bind_string == expected_bind_string_output
    