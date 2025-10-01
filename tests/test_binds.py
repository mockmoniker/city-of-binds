import pytest
from CityOfBinds import Trigger, Bind, ToggleBind, WASDBind

### Bind Tests

class TestValidBindInitialization:
    bind_under_test = Bind

    def test_init_should_set_internal_trigger_object_given_valid_trigger(self):
        # arrange
        valid_trigger = 'SHIFT+W'
        valid_slash_commands = ['powexectoggleon sprint']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, slash_commands=valid_slash_commands)
        # assert
        assert isinstance(bind._trigger, Trigger)
        assert bind._trigger.key == 'W'
        assert bind._trigger.modifier == 'SHIFT'

    def test_init_should_set_slash_commands_given_valid_slash_commands(self):
        # arrange
        valid_trigger = 'W'
        valid_slash_commands = ['powexectoggleon sprint', 'powexectoggleon super speed']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, slash_commands=valid_slash_commands)
        # assert
        assert bind.slash_commands == valid_slash_commands

    def test_init_should_set_lowercase_slash_commands_given_valid_uppercase_slash_commands(self):
        # arrange
        valid_trigger = 'W'
        uppercase_slash_commands = ['POWEXECTOGGLEON SPRINT', 'POWEXECTOGLONE SUPER SPEED']
        expected_slash_commands = ['powexectoggleon sprint', 'powexectoggleon super speed']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, slash_commands=uppercase_slash_commands)
        # assert
        assert bind.slash_commands == expected_slash_commands

class TestInvalidBindInitialization:
    bind_under_test = Bind

    def test_init_should_raise_value_error_given_empty_slash_commands(self):
        # arrange
        valid_trigger = 'W'
        invalid_slash_commands = []
        # act
        with pytest.raises(ValueError) as excinfo:
            bind = self.bind_under_test(trigger=valid_trigger, slash_commands=invalid_slash_commands)
        #  assert
        assert "Slash Commands list cannot be empty." in str(excinfo.value)

    def test_init_should_raise_value_error_given_empty_slash_command(self):
        # arrange
        valid_trigger = 'W'
        invalid_slash_commands = ['powexectoggleon sprint', '']
        # act 
        with pytest.raises(ValueError) as excinfo:
            bind = self.bind_under_test(trigger=valid_trigger, slash_commands=invalid_slash_commands)
        # assert
        assert "Slash Commands list cannot contain empty commands." in str(excinfo.value)

class TestValidBindSetters:
    bind_under_test = Bind

    def test_trigger_setter_should_set_internal_trigger_object_given_valid_trigger(self):
        # arrange
        bind = self.bind_under_test(trigger='W', slash_commands=['powexectoggleon sprint'])
        new_valid_trigger = 'SHIFT+S'
        # act
        bind.trigger = new_valid_trigger
        # assert
        assert isinstance(bind._trigger, Trigger)
        assert bind._trigger.key == 'S'
        assert bind._trigger.modifier == 'SHIFT'

    def test_set_slash_commands_should_set_slash_commands_given_valid_slash_commands(self):
        # arrange
        bind = self.bind_under_test(trigger='W', slash_commands=['powexectoggleon sprint', 'powexectoggleon super speed'])
        new_valid_slash_commands = ['powexectoggleon athletic run']
        # act
        bind.slash_commands = new_valid_slash_commands
        # assert
        assert bind.slash_commands == new_valid_slash_commands

class TestInvalidBindSetters:
    bind_under_test = Bind

    def test_set_slash_commands_should_raise_value_error_given_empty_slash_commands(self):
        # arrange
        bind = self.bind_under_test(trigger='W', slash_commands=['powexectoggleon sprint'])
        invalid_slash_commands = []
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind.slash_commands = invalid_slash_commands
    
    def test_set_slash_commands_should_raise_value_error_given_empty_slash_command(self):
        # arrange
        bind = self.bind_under_test(trigger='W', slash_commands=['powexectoggleon sprint'])
        invalid_slash_commands = ['powexectoggle super speed', '']
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot contain empty commands.*'):
            bind.slash_commands = invalid_slash_commands

class TestBindStrings:
    bind_under_test = Bind

    def test_bind_string_should_return_correct_string_given_single_valid_slash_command(self):
        # arrange
        valid_trigger = 'Q'
        valid_slash_commands = ['powexectoggleon dark nova']
        expected_bind_string = 'Q "powexectoggleon dark nova"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, slash_commands=valid_slash_commands)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_multiple_valid_slash_commands(self):
        # arrange
        valid_trigger = 'Q'
        valid_slash_commands = ['powexectoggleoff black dwarf', 'powexectoggleon dark nova']
        expected_bind_string = 'Q "powexectoggleoff black dwarf$$powexectoggleon dark nova"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, slash_commands=valid_slash_commands)
        # assert
        assert bind.bind_string == expected_bind_string

### ToggleBind Tests

class TestValidToggleBindInitializaiton(TestValidBindInitialization):
    bind_under_test = ToggleBind

    def test_init_should_set_toggle_off_powers_given_valid_powers(self):
        # arrange
        valid_trigger = 'W'
        valid_powers = ['dark nova', 'black dwarf']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=valid_powers)
        # assert
        assert bind.toggle_off_powers == valid_powers

    def test_init_should_set_toggle_on_powers_given_valid_powers(self):
        # arrange
        valid_trigger = 'W'
        valid_powers = ['super speed', 'super jump']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_on_powers=valid_powers)
        # assert
        assert bind.toggle_on_powers == valid_powers

    def test_init_should_set_auto_power_given_valid_power(self):
        # arrange
        valid_trigger = 'W'
        valid_power = 'hasten'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, auto_power=valid_power)
        # assert
        assert bind.auto_power == valid_power

class TestInvalidToggleBindInitialization(TestInvalidBindInitialization):
    bind_under_test = ToggleBind

    def test_init_should_raise_value_error_given_empty_toggle_off_powers(self):
        # arrange
        valid_trigger = 'W'
        invalid_powers = []
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=invalid_powers)

    def test_init_should_raise_value_error_given_empty_toggle_off_power(self):
        # arrange
        valid_trigger = 'W'
        invalid_powers = ['dark nova', '']
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot contain empty commands.*'):
            bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=invalid_powers)

    def test_init_should_raise_value_error_given_empty_toggle_on_powers(self):
        # arrange
        valid_trigger = 'W'
        invalid_powers = []
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind = self.bind_under_test(trigger=valid_trigger, toggle_on_powers=invalid_powers)

    def test_init_should_raise_value_error_given_empty_toggle_on_power(self):
        # arrange
        valid_trigger = 'W'
        invalid_powers = ['dark nova', '']
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot contain empty commands.*'):
            bind = self.bind_under_test(trigger=valid_trigger, toggle_on_powers=invalid_powers)

    def test_init_should_raise_value_error_given_empty_auto_power(self):
        # arrange
        valid_trigger = 'W'
        invalid_power = ''
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind = self.bind_under_test(trigger=valid_trigger, auto_power=invalid_power)

class TestValidToggleBindSetters(TestValidBindSetters):
    bind_under_test = ToggleBind

    def test_set_toggle_off_powers_should_set_toggle_off_powers_given_valid_powers(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_off_powers=['dark nova'])
        new_valid_powers = ['black dwarf']
        # act
        bind.toggle_off_powers = new_valid_powers
        # assert
        assert bind.toggle_off_powers == new_valid_powers

    def test_set_toggle_on_powers_should_set_toggle_on_powers_given_valid_powers(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_on_powers=['dark nova'])
        new_valid_powers = ['black dwarf']
        # act
        bind.toggle_on_powers = new_valid_powers
        # assert
        assert bind.toggle_on_powers == new_valid_powers

    def test_set_auto_power_should_set_auto_power_given_valid_power(self):
        # arrange
        bind = self.bind_under_test(trigger='W', auto_power='hasten')
        new_valid_power = 'inner inspiration'
        # act
        bind.auto_power = new_valid_power
        # assert
        assert bind.auto_power == new_valid_power

class TestInvalidToggleBindSetters(TestInvalidBindSetters):
    bind_under_test = ToggleBind

    def test_set_toggle_off_powers_should_raise_value_error_given_empty_toggle_off_powers(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_off_powers=['dark nova'])
        invalid_powers = []
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind.toggle_off_powers = invalid_powers

    def test_set_toggle_off_powers_should_raise_value_error_given_empty_toggle_off_power(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_off_powers=['dark nova'])
        invalid_powers = ['black dwarf', '']
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot contain empty commands.*'):
            bind.toggle_off_powers = invalid_powers

    def test_set_toggle_on_powers_should_raise_value_error_given_empty_toggle_on_powers(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_on_powers=['dark nova'])
        invalid_powers = []
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind.toggle_on_powers = invalid_powers

    def test_set_toggle_on_powers_should_raise_value_error_given_empty_toggle_on_power(self):
        # arrange
        bind = self.bind_under_test(trigger='W', toggle_on_powers=['dark nova'])
        invalid_powers = ['black dwarf', '']
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot contain empty commands.*'):
            bind.toggle_on_powers = invalid_powers

    def test_set_auto_power_should_raise_value_error_given_empty_auto_power(self):
        # arrange
        bind = self.bind_under_test(trigger='W', auto_power='hasten')
        invalid_power = ''
        # act and assert
        with pytest.raises(ValueError, match='.*Slash Commands list cannot be empty.*'):
            bind.auto_power = invalid_power

class TestToggleBindStrings(TestBindStrings):
    bind_under_test = ToggleBind

    def test_bind_string_should_return_correct_string_given_valid_toggle_off_power(self):
        # arrange
        valid_trigger = 'W'
        valid_toggle_off_power = ['dark nova']
        expected_bind_string = 'W "powexectoggleoff dark nova"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=valid_toggle_off_power)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_valid_toggle_off_powers(self):
        # arrange
        valid_trigger = 'W'
        valid_toggle_off_powers = ['dark nova', 'black dwarf']
        expected_bind_string = 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=valid_toggle_off_powers)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_valid_toggle_on_power(self):
        # arrange
        valid_trigger = 'SPACE'
        valid_toggle_on_power = ['combat jumping']
        expected_bind_string = 'SPACE "powexectoggleon combat jumping"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_on_powers=valid_toggle_on_power)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_valid_toggle_on_powers(self):
        # arrange
        valid_trigger = 'SPACE'
        valid_toggle_on_powers = ['combat jumping', 'super jump']
        expected_bind_string = 'SPACE "powexectoggleon combat jumping$$powexectoggleon super jump"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_on_powers=valid_toggle_on_powers)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_valid_auto_power(self):
        # arrange
        valid_trigger = 'W'
        valid_auto_power = 'hasten'
        expected_bind_string = 'W "powexecauto hasten"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, auto_power=valid_auto_power)
        # assert
        assert bind.bind_string == expected_bind_string

    def test_bind_string_should_return_correct_string_given_all_valid_powers(self):
        # arrange
        valid_trigger = 'SPACE'
        valid_toggle_off_powers = ['dark nova', 'black dwarf']
        valid_toggle_on_powers = ['combat jumping', 'super jump']
        valid_auto_power = 'hasten'
        expected_bind_string = 'SPACE "powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon combat jumping$$powexectoggleon super jump$$powexecauto hasten"'
        # act
        bind = self.bind_under_test(trigger=valid_trigger, toggle_off_powers=valid_toggle_off_powers, toggle_on_powers=valid_toggle_on_powers , auto_power=valid_auto_power)
        # assert
        assert bind.bind_string == expected_bind_string

### WASDBind Tests

class TestValidWASDBindInitializaiton(TestValidToggleBindInitializaiton):
    bind_under_test = WASDBind

    def test_init_should_set_movement_powers_given_valid_powers(self):
        # arrange
        valid_trigger = 'W'
        valid_movement_powers = ['sprint', 'super speed']
        # act
        bind = self.bind_under_test(trigger=valid_trigger, movement_powers=valid_movement_powers)
        # assert
        assert bind.movement_powers == valid_movement_powers