import pytest
from CityOfBinds import SlashCommand, Trigger, Power, Bind, ToggleBind, WASDBind

### Bind Tests ###

# Bind Initialization Tests
class TestBindInitialization:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_init_should_set_internal_trigger_given_trigger_string(self):
        # arrange
        trigger_string = 'SHIFT+SPACE'

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=trigger_string)

        # assert
        assert bind._trigger == Trigger('SHIFT+SPACE')

    def test_init_should_set_internal_slash_commands_given_slash_commands_string_list(self):
        # arrange
        slash_commands_string_list = ['+forward', 'powexectoggleon super speed']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_string_list=slash_commands_string_list)

        # assert
        assert bind._slash_commands == [SlashCommand('+forward'), SlashCommand('powexectoggleon super speed')]

# Bind Property Tests
class TestBindTriggerProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_trigger_getter_should_return_trigger(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string="SHIFT+SPACE")

        # act
        trigger = bind.trigger

        # assert
        assert trigger == Trigger('SHIFT+SPACE')

    def test_trigger_setter_should_set_trigger_given_new_trigger_string(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)
        new_trigger_string = 'SHIFT+SPACE'

        # act
        bind.trigger = new_trigger_string

        # assert
        assert bind.trigger == Trigger('SHIFT+SPACE')

class TestBindSlashCommandsProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_slash_commands_getter_should_return_list_of_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_string_list=['+forward', 'powexectoggleon super speed'])

        # act
        list_of_slash_commands = bind.slash_commands

        # assert
        assert list_of_slash_commands == [SlashCommand('+forward'), SlashCommand('powexectoggleon super speed')]

    def test_slash_commands_setter_should_set_slash_commands_given_new_slash_commands_string_list(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)
        new_slash_commands_string_list = ['+forward', 'powexectoggleon super speed']

        # act
        bind.slash_commands = new_slash_commands_string_list

        # assert
        assert bind.slash_commands == [SlashCommand('+forward'), SlashCommand('powexectoggleon super speed')]

class TestBindBindStringProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_string_should_return_bind_string_with_single_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_string_list=['+forward'])
        # act
        bind_string_with_single_command = bind.bind_string
        # assert
        assert bind_string_with_single_command == 'W "+forward"'

    def test_bind_string_should_return_bind_string_with_multiple_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_string_list=['+forward', 'powexectoggleon super speed'])
        # act
        bind_string = bind.bind_string
        # assert
        assert bind_string == 'W "+forward$$powexectoggleon super speed"'

class TestBindBindLengthProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_length_should_return_length_of_bind(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='Q', slash_commands_string_list=['powexectoggleoff black dwarf', 'powexectoggleon dark nova'])

        # act
        bind_length = bind.bind_length

        # assert
        assert bind_length == len('Q "powexectoggleoff black dwarf$$powexectoggleon dark nova"')

# Bind Method Tests
class TestBindValidateMethod:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'
    VALID_SLASH_COMMAND_LIST = ['+forward', 'powexectoggleon super speed']

    def test_validate_should_pass_given_valid_bind(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_string_list=self.VALID_SLASH_COMMAND_LIST)

        # act / assert
        bind.validate()  # should not raise an exception

    def test_validate_should_raise_value_error_given_bind_with_no_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)

        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()

        # assert
        assert "Bind must contain one or more slash commands." in str(excinfo.value)

    def test_validate_should_raise_value_error_given_bind_length_exceeding_maximum_length(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_string_list=[f"l {'A'*250}"]) # 256 characters long

        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()

        # assert
        assert "Bind exceeds maximum length of 255 characters." in str(excinfo.value)

class TestBindIsEmptyMethod:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'
    VALID_SLASH_COMMAND_LIST = ['powexectoggleon super speed']

    def test_is_empty_should_return_true_given_bind_with_no_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is True

    def test_is_empty_should_return_false_given_bind_with_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_string_list=self.VALID_SLASH_COMMAND_LIST)

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is False

### ToggleBind Tests ###

# ToggleBind Initialization Tests
class TestToggleBindInitialization(TestBindInitialization):
    BIND_UNDER_TEST = ToggleBind

    def test_init_should_set_internal_powers_given_toggle_off_powers_string_list(self):
        # arrange
        toggle_off_powers_string_list = ['dark nova', 'black dwarf']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_off_powers_string_list=toggle_off_powers_string_list)

        # assert
        assert bind._toggle_off_powers == [Power('dark nova'), Power('black dwarf')]

    def test_init_should_set_internal_powers_given_toggle_on_powers_string_list(self):
        # arrange
        toggle_on_powers_string_list = ['sprint', 'super jump']
        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_on_powers_string_list=toggle_on_powers_string_list)

        # assert
        assert bind._toggle_on_powers == [Power('sprint'), Power('super jump')]

# ToggleBind Property Tests
class TestToggleBindTriggerProperty(TestBindTriggerProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindSlashCommandsProperty(TestBindSlashCommandsProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindBindStringProperty(TestBindBindStringProperty):
    BIND_UNDER_TEST = ToggleBind

    def test_bind_string_should_return_bind_string_given_single_toggle_off_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleoff dark nova"'

    def test_bind_string_should_return_bind_string_given_multiple_toggle_off_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf"'

    def test_bind_string_should_return_bind_string_given_single_toggle_on_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_string_list=['sprint'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleon sprint"'

    def test_bind_string_should_return_bind_string_given_multiple_toggle_on_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_string_list=['sprint', 'super speed'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleon sprint$$powexectoggleon super speed"'

    def test_bind_string_should_return_bind_string_given_auto_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', auto_power_string='hasten')

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexecauto hasten"'

    def test_bind_string_should_return_bind_string_given_all_defined_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'], toggle_on_powers_string_list=['sprint', 'super speed'], auto_power_string='hasten')
        
        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten"'

    def test_bind_string_should_return_bind_string_given_all_defined_powers_and_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'], toggle_on_powers_string_list=['sprint', 'super speed'], auto_power_string='hasten', slash_commands_string_list=['powexectoggleon tough', 'powexectoggleon weave'])
        
        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$powexectoggleon tough$$powexectoggleon weave"'

class TestToggleBindBindLengthProperty(TestBindBindLengthProperty):
    BIND_UNDER_TEST = ToggleBind

# ToggleBind Method Tests
class TestToggleBindValidateMethod(TestBindValidateMethod):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindIsEmptyMethod(TestBindIsEmptyMethod):
    BIND_UNDER_TEST = ToggleBind

    def test_is_empty_should_return_false_given_toggle_off_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_off_powers_string_list=['dark nova'])

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is False

    def test_is_empty_should_return_false_given_toggle_on_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_on_powers_string_list=['sprint'])

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is False

    def test_is_empty_should_return_false_given_auto_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, auto_power_string='hasten')

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is False

### WASDBind Tests ###

# WASDBind Initialization Tests
class TestWASDBindInitialization(TestToggleBindInitialization):
    BIND_UNDER_TEST = WASDBind

    def test_init_should_set_internal_movement_powers_given_movement_powers_string_list(self):
        # arrange
        movement_powers_string_list = ['sprint', 'super speed']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, movement_powers_string_list=movement_powers_string_list)

        # assert
        assert bind._movement_powers == [Power('sprint'), Power('super speed')]

# WASDBind Property Tests
class TestWASDBindTriggerProperty(TestToggleBindTriggerProperty):
    BIND_UNDER_TEST = WASDBind

class TestWASDBindSlashCommandsProperty(TestToggleBindSlashCommandsProperty):
    BIND_UNDER_TEST = WASDBind

class TestWASDBindBindStringProperty(TestToggleBindBindStringProperty):
    BIND_UNDER_TEST = WASDBind

    def test_bind_string_should_return_bind_string_with_single_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_string_list=['powexectoggleon super speed'])

        # act
        bind_string_with_single_command = bind.bind_string

        # assert
        assert bind_string_with_single_command == 'W "+forward$$powexectoggleon super speed"'

    def test_bind_string_should_return_bind_string_with_multiple_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_string_list=['powexectoggleon super speed', 'powexecauto hasten'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleon super speed$$powexecauto hasten"'

    def test_bind_string_should_return_bind_string_given_single_toggle_off_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleoff dark nova"'

    def test_bind_string_should_return_bind_string_given_multiple_toggle_off_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf"'

    def test_bind_string_should_return_bind_string_given_single_toggle_on_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_string_list=['sprint'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleon sprint"'

    def test_bind_string_should_return_bind_string_given_multiple_toggle_on_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_string_list=['sprint', 'super speed'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleon sprint$$powexectoggleon super speed"'

    def test_bind_string_should_return_bind_string_given_auto_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', auto_power_string='hasten')

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexecauto hasten"'

    def test_bind_string_should_return_bind_string_given_single_movement_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', movement_powers_string_list=['sprint'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleon sprint"'

    def test_bind_string_should_return_bind_string_given_multiple_movement_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', movement_powers_string_list=['sprint', 'super speed'])

        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleon sprint$$powexectoggleon super speed"'

    def test_bind_string_should_return_bind_string_given_all_defined_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'], movement_powers_string_list=['sprint', 'super speed'], toggle_on_powers_string_list=['tough', 'weave'], auto_power_string='hasten')
        
        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexectoggleon tough$$powexectoggleon weave$$powexecauto hasten"'

    def test_bind_string_should_return_bind_string_given_all_defined_powers_and_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'], movement_powers_string_list=['sprint', 'super speed'], toggle_on_powers_string_list=['tough', 'weave'], auto_power_string='hasten', slash_commands_string_list=['powexectoggleon leadership', 'powexectoggleon tactics'])
        
        # act
        bind_string = bind.bind_string

        # assert
        assert bind_string == 'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexectoggleon tough$$powexectoggleon weave$$powexecauto hasten$$powexectoggleon leadership$$powexectoggleon tactics"'

class TestWASDBindBindLengthProperty(TestBindBindLengthProperty):
    BIND_UNDER_TEST = WASDBind

    def test_bind_length_should_return_length_of_bind_including_forward_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_string_list=['dark nova', 'black dwarf'], movement_powers_string_list=['sprint', 'super speed'], toggle_on_powers_string_list=['tough', 'weave'], auto_power_string='hasten', slash_commands_string_list=['powexectoggleon leadership', 'powexectoggleon tactics'])

        # act
        bind_length = bind.bind_length

        # assert
        assert bind_length == len('W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexectoggleon tough$$powexectoggleon weave$$powexecauto hasten$$powexectoggleon leadership$$powexectoggleon tactics"')

# WASDBind Method Tests
class TestWASDBindValidateMethod(TestToggleBindValidateMethod):
    BIND_UNDER_TEST = WASDBind

class TestWASDBindIsEmptyMethod(TestToggleBindIsEmptyMethod):
    BIND_UNDER_TEST = WASDBind

    def test_is_empty_should_return_false_given_movement_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, movement_powers_string_list=['sprint'])

        # act
        is_empty = bind.is_empty()

        # assert
        assert is_empty is False
