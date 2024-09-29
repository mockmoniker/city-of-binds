import pytest
from CityOfBinds import WASDBind
from scenarios import Scenarios

invalid_triggers = [
    "",
    "trigger with space",
]

class TestValidWASDBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_wasd_trigger_scenarios)
    def test_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = WASDBind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_direciton", Scenarios.valid_set_wasd_direction_scenarios)
    def test_init_should_set_direction_given_valid_trigger(self, valid_trigger_input, expected_trigger_direciton):
        bind = WASDBind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind._direction == expected_trigger_direciton

    @pytest.mark.parametrize("valid_slash_command_input, expected_slash_command_output", Scenarios.valid_set_slash_commands_scenarios)
    def test_init_should_set_slash_command_given_valid_slash_command(self, valid_slash_command_input, expected_slash_command_output):
        bind = WASDBind(trigger="w", slash_commands=valid_slash_command_input)
        assert bind.slash_commands == expected_slash_command_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", Scenarios.valid_set_powers_scenarios)
    def test_init_should_set_toggle_off_powers_given_valid_powers(self, valid_power_input, expected_power_output):
        bind = WASDBind(trigger="w", toggle_off_powers=valid_power_input)
        assert bind.toggle_off_powers == expected_power_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", Scenarios.valid_set_powers_scenarios)
    def test_init_should_set_movement_powers_given_valid_powers(self, valid_power_input, expected_power_output):
        bind = WASDBind(trigger="w", movement_powers=valid_power_input)
        assert bind.movement_powers == expected_power_output

    @pytest.mark.parametrize("valid_power_input, expected_power_output", Scenarios.valid_set_powers_scenarios)
    def test_init_should_set_toggle_on_powers_given_valid_powers(self, valid_power_input, expected_power_output):
        bind = WASDBind(trigger="w", toggle_on_powers=valid_power_input)
        assert bind.toggle_on_powers == expected_power_output

    @pytest.mark.parametrize("valid_auto_power_input, expected_auto_power_output", Scenarios.valid_set_auto_power_scenarios)
    def test_init_should_set_auto_power_given_valid_auto_power(self, valid_auto_power_input, expected_auto_power_output):
        bind = WASDBind(trigger="w", auto_power=valid_auto_power_input)
        assert bind.auto_power == expected_auto_power_output

class TestValidWASDBindSetters:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", Scenarios.valid_set_wasd_trigger_scenarios)
    def test_set_trigger_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = WASDBind(trigger="w", slash_commands=["command"])
        bind.trigger = valid_trigger_input
        assert bind.trigger == expected_trigger_output

    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_direciton", Scenarios.valid_set_wasd_direction_scenarios)
    def test_set_trigger_should_set_direction_given_valid_trigger(self, valid_trigger_input, expected_trigger_direciton):
        bind = WASDBind(trigger="w", slash_commands=["command"])
        bind.trigger = valid_trigger_input
        assert bind._direction == expected_trigger_direciton