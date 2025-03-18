import pytest
import test_ToggleBind
from CityOfBinds import WASDBind
from parameters.test_WASDBind_parameters import TestWASDBindParameters

bind_under_test = WASDBind

class TestValidWASDBindInitializaiton(test_ToggleBind.TestValidToggleBindInitializaiton):
    bind_under_test = WASDBind
    default_trigger = "w"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", TestWASDBindParameters.test_init_should_set_trigger_given_valid_trigger_parameters)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = self.bind_under_test(trigger=valid_trigger_input, slash_commands=self.default_slash_commands)
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_trigger_input, expected_direction_output", TestWASDBindParameters.test_init_should_set_direction_given_valid_trigger_parameters)
    def test_init_should_set_direction_given_valid_trigger(self, valid_trigger_input, expected_direction_output):
        bind = self.bind_under_test(trigger=valid_trigger_input, slash_commands=self.default_slash_commands)
        assert bind._direction == expected_direction_output

    #@pytest.mark.parametrize("valid_powers_input, expected_powers_output", TestWASDBindParameters.valid_set_powers_scenarios)
    #def test_init_should_set_movement_powers_given_valid_powers(self, valid_powers_input, expected_powers_output):
    #    bind = self.bind_under_test(trigger=self.default_trigger, movement_powers=valid_powers_input)
    #    assert bind.movement_powers == expected_powers_output

class TestValidWASDBindSetters(test_ToggleBind.TestValidToggleBindSetters):
    bind_under_test = WASDBind
    default_trigger = "w"
    default_slash_commands = ["command"]

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", TestWASDBindParameters.test_set_trigger_should_set_trigger_given_valid_trigger_parameters)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_direciton", TestWASDBindParameters.test_set_trigger_should_set_direction_given_valid_trigger_parameters)
    def test_set_trigger_should_set_direction_given_valid_trigger(self, valid_trigger_input, expected_trigger_direciton):
        bind = self.bind_under_test(trigger=self.default_trigger, slash_commands=self.default_slash_commands)
        bind.trigger = valid_trigger_input
        assert bind._direction == expected_trigger_direciton
