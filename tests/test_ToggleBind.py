import pytest
import test_Bind
from CityOfBinds import ToggleBind
from scenarios import Scenarios

bind_under_test = ToggleBind

class TestValidToggleBindInitializaiton(test_Bind.TestValidBindInitializaiton):
    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", Scenarios.valid_set_powers_scenarios)
    def test_init_should_set_toggle_off_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = bind_under_test(trigger="w", toggle_off_powers=valid_powers_input)
        assert bind.toggle_off_powers == expected_powers_output

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", Scenarios.valid_set_powers_scenarios)
    def test_init_should_set_toggle_on_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = bind_under_test(trigger="w", toggle_on_powers=valid_powers_input)
        assert bind.toggle_on_powers == expected_powers_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", Scenarios.valid_set_power_scenarios)
    def test_init_should_set_auto_power_given_valid_auto_power(self, valid_power_input, expected_power_output):
        bind = bind_under_test(trigger="w", auto_power=valid_power_input)
        assert bind.auto_power == expected_power_output

class TestInvalidToggleBindInitialization(test_Bind.TestInvalidBindInitialization):
    @pytest.mark.parametrize("invalid_powers_input, expected_error_message", Scenarios.invalid_set_powers_scenarios)
    def test_init_should_raise_value_error_given_invalid_toggle_off_powers(self, invalid_powers_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = bind_under_test(trigger="w", toggle_off_powers=invalid_powers_input)

    @pytest.mark.parametrize("invalid_powers_input, expected_error_message", Scenarios.invalid_set_powers_scenarios)
    def test_init_should_raise_value_error_given_invalid_toggle_on_powers(self, invalid_powers_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = bind_under_test(trigger="w", toggle_on_powers=invalid_powers_input)

    @pytest.mark.parametrize("invalid_power_input, expected_error_message", Scenarios.invalid_set_power_scenarios)
    def test_init_should_raise_value_error_given_invalid_auto_power(self, invalid_power_input, expected_error_message):
        with pytest.raises(ValueError, match=f".*{expected_error_message}.*"):
            bind = bind_under_test(trigger="w", auto_power=invalid_power_input)

class TestValidToggleBindSetters(test_Bind.TestValidBindSetters):
    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", Scenarios.valid_set_powers_scenarios)
    def test_set_toggle_off_powers_should_set_toggle_off_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = bind_under_test(trigger="w", toggle_off_powers=["power"])
        bind.toggle_off_powers = valid_powers_input
        assert bind.toggle_off_powers == expected_powers_output

    @pytest.mark.parametrize("valid_powers_input, expected_powers_output", Scenarios.valid_set_powers_scenarios)
    def test_set_toggle_on_powers_should_set_toggle_on_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
        bind = bind_under_test(trigger="w", toggle_on_powers=["power"])
        bind.toggle_on_powers = valid_powers_input
        assert bind.toggle_on_powers == expected_powers_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", Scenarios.valid_set_power_scenarios)
    def test_set_auto_power_should_set_auto_power_given_valid_auto_power(self, valid_power_input, expected_power_output):
        bind = bind_under_test(trigger="w", auto_power="power")
        bind.auto_power = valid_power_input
        assert bind.auto_power == expected_power_output