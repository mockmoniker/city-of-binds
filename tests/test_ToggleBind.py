import pytest
import test_Bind
from CityOfBinds import ToggleBind
from parameters.test_ToggleBind_parameters import TestToggleBindParameters

class TestValidToggleBindInitializaiton(test_Bind.TestValidBindInitializaiton):
    bind_under_test = ToggleBind
    default_trigger = "t"

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", TestToggleBindParameters.test_init_should_set_toggle_off_powers_given_valid_powers_parameters)
    def test_init_should_set_toggle_off_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = self.bind_under_test(trigger=self.default_trigger, toggle_off_powers=valid_powers_input)
        assert bind.toggle_off_powers == expected_powers_output

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", TestToggleBindParameters.test_init_should_set_toggle_on_powers_given_valid_powers_parameters)
    def test_init_should_set_toggle_on_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = self.bind_under_test(trigger=self.default_trigger, toggle_on_powers=valid_powers_input)
        assert bind.toggle_on_powers == expected_powers_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", TestToggleBindParameters.test_init_should_set_auto_power_given_valid_auto_power_parameters)
    def test_init_should_set_auto_power_given_valid_auto_power(self, valid_power_input, expected_power_output):
        bind = self.bind_under_test(trigger=self.default_trigger, auto_power=valid_power_input)
        assert bind.auto_power == expected_power_output

class TestInvalidToggleBindInitialization(test_Bind.TestInvalidBindInitialization):
    bind_under_test = ToggleBind
    default_trigger = "t"
    default_slash_commands = ["command"]
    default_powers = ["power"]
    default_power = "power"

    @pytest.mark.parametrize("invalid_powers_input, expected_error_message", TestToggleBindParameters.test_init_should_raise_value_error_given_invalid_toggle_off_powers_parameters)
    def test_init_should_raise_value_error_given_invalid_toggle_off_powers(self, invalid_powers_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = self.bind_under_test(trigger=self.default_trigger, toggle_off_powers=invalid_powers_input)

    @pytest.mark.parametrize("invalid_powers_input, expected_error_message", TestToggleBindParameters.test_init_should_raise_value_error_given_invalid_toggle_on_powers_parameters)
    def test_init_should_raise_value_error_given_invalid_toggle_on_powers(self, invalid_powers_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = self.bind_under_test(trigger=self.default_trigger, toggle_on_powers=invalid_powers_input)

    @pytest.mark.parametrize("invalid_power_input, expected_error_message", TestToggleBindParameters.test_init_should_raise_value_error_given_invalid_auto_power_parameters)
    def test_init_should_raise_value_error_given_invalid_auto_power(self, invalid_power_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = self.bind_under_test(trigger=self.default_trigger, auto_power=invalid_power_input)

class TestValidToggleBindSetters(test_Bind.TestValidBindSetters):
    bind_under_test = ToggleBind
    default_trigger = "t"
    default_slash_commands = ["command"]
    default_powers = ["power"]
    default_power = "power"

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", TestToggleBindParameters.test_set_toggle_off_powers_should_set_toggle_off_powers_given_valid_powers_parameters)
    def test_set_toggle_off_powers_should_set_toggle_off_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = self.bind_under_test(trigger=self.default_trigger, toggle_off_powers=self.default_powers)
        bind.toggle_off_powers = valid_powers_input
        assert bind.toggle_off_powers == expected_powers_output

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", TestToggleBindParameters.test_set_toggle_on_powers_should_set_toggle_on_powers_given_valid_powers_parameters)
    def test_set_toggle_on_powers_should_set_toggle_on_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = self.bind_under_test(trigger=self.default_trigger, toggle_on_powers=self.default_powers)
        bind.toggle_on_powers = valid_powers_input
        assert bind.toggle_on_powers == expected_powers_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", TestToggleBindParameters.test_set_auto_power_should_set_auto_power_given_valid_auto_power_parameters)
    def test_set_auto_power_should_set_auto_power_given_valid_auto_power(self, valid_power_input, expected_power_output):
        bind = self.bind_under_test(trigger=self.default_trigger, auto_power=self.default_power)
        bind.auto_power = valid_power_input
        assert bind.auto_power == expected_power_output