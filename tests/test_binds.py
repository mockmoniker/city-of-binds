import pytest
from CityOfBinds import Bind, ToggleBind, WASDBind
from parameters.test_binds_parameters import TestBindParameters, TestToggleBindParameters, TestWASDBindParameters

### Bind Tests

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

### ToggleBind Tests

class TestValidToggleBindInitializaiton(TestValidBindInitializaiton):
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

class TestInvalidToggleBindInitialization(TestInvalidBindInitialization):
    bind_under_test = ToggleBind
    default_trigger = "t"

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

class TestValidToggleBindSetters(TestValidBindSetters):
    bind_under_test = ToggleBind
    default_trigger = "t"
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

### WASDBind Tests

class TestValidWASDBindInitializaiton(TestValidToggleBindInitializaiton):
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

class TestValidWASDBindSetters(TestValidToggleBindSetters):
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
