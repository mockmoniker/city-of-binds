import pytest
from CityOfBinds import SlashCommand, Trigger, Power, Bind, ToggleBind, WASDBind

### Bind Tests

class TestBindInitialization:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_init_should_create_and_set_trigger_object_given_valid_trigger_string(self):
        # arrange
        valid_trigger_string = 'SHIFT+SPACE'

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=valid_trigger_string)

        # assert
        assert isinstance(bind._trigger, Trigger)
        assert bind._trigger.key == 'SPACE'
        assert bind._trigger.modifier == 'SHIFT'

    def test_init_should_create_and_set_slash_command_objects_given_valid_slash_commands_list(self):
        # arrange
        valid_slash_commands_list = ['+forward', 'powexectoggleon super speed']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_list=valid_slash_commands_list)

        # assert
        assert all(isinstance(slash_command, SlashCommand) for slash_command in bind._slash_commands)
        assert [slash_command.slash_command_string for slash_command in bind._slash_commands] == ['+forward', 'powexectoggleon super speed']
        assert bind._slash_commands[0].prefix == '+'
        assert bind._slash_commands[0].command == 'forward'
        assert bind._slash_commands[1].command == 'powexectoggleon'
        assert bind._slash_commands[1].args == 'super speed'

class TestBindTriggerProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_trigger_getter_should_return_trigger_string(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string="SHIFT+SPACE")

        # act
        trigger = bind.trigger

        # assert
        assert trigger == 'SHIFT+SPACE'

    def test_trigger_setter_should_set_trigger_given_new_valid_trigger_string(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)
        new_valid_trigger_string = 'SHIFT+SPACE'

        # act
        bind.trigger = new_valid_trigger_string

        # assert
        assert bind.trigger == 'SHIFT+SPACE'

class TestBindTriggerKeyProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_trigger_key_getter_should_return_trigger_key(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string="SHIFT+SPACE")

        # act
        trigger_key = bind.trigger_key

        # assert
        assert trigger_key == 'SPACE'

    def test_trigger_key_setter_should_set_trigger_key_given_new_valid_key(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)
        new_valid_key = 'SPACE'

        # act
        bind.trigger_key = new_valid_key

        # assert
        assert bind.trigger_key == 'SPACE'

class TestBindTriggerModifierProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_trigger_modifier_getter_should_return_trigger_modifier(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string="SHIFT+SPACE")

        # act
        trigger_modifier = bind.trigger_modifier

        # assert
        assert trigger_modifier == 'SHIFT'

    def test_trigger_modifier_setter_should_set_trigger_modifier_given_new_valid_modifier(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)
        new_valid_modifier = 'SHIFT'

        # act
        bind.trigger_modifier = new_valid_modifier

        # assert
        assert bind.trigger_modifier == 'SHIFT'

class TestBindSlashCommandsProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = 'W'

    def test_slash_commands_getter_should_return_list_of_slash_command_strings(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, slash_commands_list=['+forward', 'powexectoggleon super speed'])

        # act
        list_of_slash_commands_strings = bind.slash_commands

        # assert
        assert list_of_slash_commands_strings == ['+forward', 'powexectoggleon super speed']

    def test_slash_commands_setter_should_set_slash_commands_given_new_valid_slash_commands_list(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER)

        # act
        bind.slash_commands = ['+forward', 'powexectoggleon super speed']

        # assert
        assert bind.slash_commands == ['+forward', 'powexectoggleon super speed']

class TestBindBindStringProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_string_should_return_correctly_formatted_bind_string_with_single_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_list=['+forward'])
        # act
        correctly_formatted_bind_string_with_single_command = bind.bind_string
        # assert
        assert correctly_formatted_bind_string_with_single_command == 'W "+forward"'

    def test_bind_string_should_return_correctly_formatted_bind_string_with_multiple_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_list=['+forward', 'powexectoggleon super speed'])
        # act
        correctly_formatted_bind_string = bind.bind_string
        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleon super speed"'

class TestBindBindLengthProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_length_should_return_length_of_formatted_bind_string(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='Q', slash_commands_list=['powexectoggleoff black dwarf', 'powexectoggleon dark nova'])
        # act
        bind_length = bind.bind_length
        # assert
        assert bind_length == len('Q "powexectoggleoff black dwarf$$powexectoggleon dark nova"')

class TestBindValidateMethod:
    BIND_UNDER_TEST = Bind
    VALID_BIND_TRIGGER = 'W'
    VALID_SLASH_COMMAND_LIST = ['+forward', 'powexectoggleon super speed']

    def test_validate_should_pass_given_valid_bind(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_BIND_TRIGGER, slash_commands_list=self.VALID_SLASH_COMMAND_LIST)

        # act / assert
        bind.validate()  # should not raise an exception

    def test_validate_should_raise_value_error_given_bind_with_no_slash_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_BIND_TRIGGER, slash_commands_list=[])

        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()

        # assert
        assert "Bind must contain one or more slash commands." in str(excinfo.value)

    def test_validate_should_raise_value_error_given_bind_length_exceeding_maximum_length(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_BIND_TRIGGER, slash_commands_list=[f"l {'A'*250}"]) # 256 characters long

        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()

        # assert
        assert "Bind exceeds maximum length of 255 characters." in str(excinfo.value)

### ToggleBind Tests

class TestToggleBindInitialization(TestBindInitialization):
    BIND_UNDER_TEST = ToggleBind

    def test_init_should_create_and_set_power_objects_given_valid_toggle_off_powers_list(self):
        # arrange
        valid_toggle_off_powers_list = ['dark nova', 'black dwarf']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_off_powers_list=valid_toggle_off_powers_list)

        # assert
        assert all(isinstance(power, Power) for power in bind._toggle_off_powers)
        assert [power.power_string for power in bind._toggle_off_powers] == ['dark nova', 'black dwarf']
    
    def test_init_should_create_and_set_power_objects_given_valid_toggle_on_powers_list(self):
        # arrange
        valid_toggle_on_powers_list = ['sprint', 'super jump']

        # act
        bind = self.BIND_UNDER_TEST(trigger_string=self.VALID_TRIGGER, toggle_on_powers_list=valid_toggle_on_powers_list)

        # assert
        assert all(isinstance(power, Power) for power in bind._toggle_on_powers)
        assert [power.power_string for power in bind._toggle_on_powers] == ['sprint', 'super jump']

class TestToggleBindTriggerProperty(TestBindTriggerProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindTriggerKeyProperty(TestBindTriggerKeyProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindTriggerModifierProperty(TestBindTriggerModifierProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindSlashCommandsProperty(TestBindSlashCommandsProperty):
    BIND_UNDER_TEST = ToggleBind

class TestToggleBindBindStringProperty(TestBindBindStringProperty):
    BIND_UNDER_TEST = ToggleBind

    def test_bind_string_should_return_correctly_formatted_bind_string_given_single_toggle_off_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexectoggleoff dark nova"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_multiple_toggle_off_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova', 'black dwarf'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_single_toggle_on_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_list=['sprint'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexectoggleon sprint"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_multiple_toggle_on_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_list=['sprint', 'super speed'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexectoggleon sprint$$powexectoggleon super speed"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_auto_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', auto_power_string='hasten')

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexecauto hasten"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_all_defined_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova', 'black dwarf'], toggle_on_powers_list=['sprint', 'super speed'], auto_power_string='hasten')
        
        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten"'

### WASDBind Tests

class TestWASDBindInitialization(TestToggleBindInitialization):
    BIND_UNDER_TEST = WASDBind

    def test_init_should_set_movement_powers_given_valid_powers(self):
        # arrange
        valid_trigger = 'W'
        valid_movement_powers = ['sprint', 'super speed']
        # act
        bind = self.BIND_UNDER_TEST(trigger_string=valid_trigger, movement_powers_list=valid_movement_powers)
        # assert
        assert bind.movement_powers == valid_movement_powers

class TestWASDBindBindStringProperty(TestToggleBindBindStringProperty):
    BIND_UNDER_TEST = WASDBind

    def test_bind_string_should_return_correctly_formatted_bind_string_with_single_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W')
        # act
        correctly_formatted_bind_string_with_single_command = bind.bind_string
        # assert
        assert correctly_formatted_bind_string_with_single_command == 'W "+forward"'

    def test_bind_string_should_return_correctly_formatted_bind_string_with_multiple_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', slash_commands_list=['powexectoggleon super speed'])
        # act
        correctly_formatted_bind_string = bind.bind_string
        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleon super speed"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_single_toggle_off_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleoff dark nova"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_multiple_toggle_off_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova', 'black dwarf'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_single_toggle_on_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_list=['sprint'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleon sprint"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_multiple_toggle_on_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_on_powers_list=['sprint', 'super speed'])

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleon sprint$$powexectoggleon super speed"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_auto_power(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', auto_power_string='hasten')

        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexecauto hasten"'

    def test_bind_string_should_return_correctly_formatted_bind_string_given_all_defined_powers(self):
        # arrange
        bind = self.BIND_UNDER_TEST(trigger_string='W', toggle_off_powers_list=['dark nova', 'black dwarf'], toggle_on_powers_list=['sprint', 'super speed'], auto_power_string='hasten')
        
        # act
        correctly_formatted_bind_string = bind.bind_string

        # assert
        assert correctly_formatted_bind_string == 'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten"'
