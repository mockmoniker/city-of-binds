import pytest
from CityOfBinds import Bind, WASDBind
from CityOfBinds.src.game.utils import _Trigger, _WASDTrigger
from CityOfBinds.src.game.utils import SlashCommand, _CommandGroup

### Bind Tests ###


# Bind Initialization Tests
class TestBindInitialization:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = "W"

    def test_init_should_set_internal_trigger_given_trigger_string(self):
        # arrange
        trigger_string = "SHIFT+SPACE"
        # act
        bind = self.BIND_UNDER_TEST(trigger_string)
        # assert
        assert bind._trigger == _Trigger("SHIFT+SPACE")

    def test_init_should_set_internal_commands_given_commands_string_list(self):
        # arrange
        commands_string_list = ["+forward", "powexectoggleon super speed"]
        # act
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER, commands_string_list)
        # assert
        assert bind._commands == _CommandGroup(
            [
                "+forward",
                "powexectoggleon super speed",
            ]
        )


# Bind Property Tests
class TestBindTriggerProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = "W"

    def test_trigger_getter_should_return_trigger(self):
        # arrange
        bind = self.BIND_UNDER_TEST("SHIFT+SPACE")
        # act
        trigger = bind.trigger
        # assert
        assert trigger == _Trigger("SHIFT+SPACE")

    def test_trigger_setter_should_set_trigger_given_new_trigger_string(self):
        # arrange
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER)
        new_trigger_string = "SHIFT+SPACE"
        # act
        bind.trigger = new_trigger_string
        # assert
        assert bind.trigger == _Trigger("SHIFT+SPACE")


class TestBindCommandsProperty:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = "W"

    def test_commands_getter_should_return_list_of_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(
            self.VALID_TRIGGER, ["+forward", "powexectoggleon super speed"]
        )
        # act
        list_of_commands = bind.commands
        # assert
        assert list_of_commands == _CommandGroup(
            ["+forward", "powexectoggleon super speed"]
        )

    def test_commands_setter_should_set_commands_given_new_commands_string_list(self):
        # arrange
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER)
        new_commands_string_list = ["+forward", "powexectoggleon super speed"]
        # act
        bind.commands = new_commands_string_list
        # assert
        assert bind.commands == _CommandGroup(
            ["+forward", "powexectoggleon super speed"]
        )


class TestBindBindStringProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_string_should_return_bind_string_with_single_command(self):
        # arrange
        bind = self.BIND_UNDER_TEST("W", ["+forward"])
        # act
        bind_string_with_single_command = bind.bind_string
        # assert
        assert bind_string_with_single_command == 'W "+forward"'

    def test_bind_string_should_return_bind_string_with_multiple_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST("W", ["+forward", "powexectoggleon super speed"])
        # act
        bind_string = bind.bind_string
        # assert
        assert bind_string == 'W "+forward$$powexectoggleon super speed"'


class TestBindBindLengthProperty:
    BIND_UNDER_TEST = Bind

    def test_bind_length_should_return_length_of_bind(self):
        # arrange
        bind = self.BIND_UNDER_TEST(
            "Q", ["powexectoggleoff black dwarf", "powexectoggleon dark nova"]
        )
        # act
        bind_length = bind.bind_length
        # assert
        assert bind_length == len(
            'Q "powexectoggleoff black dwarf$$powexectoggleon dark nova"'
        )


# Bind Method Tests
class TestBindValidateMethod:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = "W"
    VALID_COMMAND_LIST = ["+forward", "powexectoggleon super speed"]

    def test_validate_should_pass_given_valid_bind(self):
        # arrange
        valid_bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER, self.VALID_COMMAND_LIST)
        # act / assert
        valid_bind.validate()  # should not raise an exception

    def test_validate_should_raise_value_error_given_bind_with_no_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER)
        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()
        # assert
        assert "Bind must contain one or more commands." in str(excinfo.value)

    def test_validate_should_raise_value_error_given_bind_length_exceeding_maximum_length(
        self,
    ):
        # arrange
        bind = self.BIND_UNDER_TEST(
            self.VALID_TRIGGER, [f"l {'A'*250}"]
        )  # 256 characters long
        # act
        with pytest.raises(ValueError) as excinfo:
            bind.validate()
        # assert
        assert "Bind exceeds maximum length of 255 characters." in str(excinfo.value)


class TestBindIsEmptyMethod:
    BIND_UNDER_TEST = Bind
    VALID_TRIGGER = "W"
    VALID_COMMAND_LIST = ["powexectoggleon super speed"]

    def test_is_empty_should_return_true_given_bind_with_no_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER)
        # act
        is_empty = bind.is_empty()
        # assert
        assert is_empty is True

    def test_is_empty_should_return_false_given_bind_with_commands(self):
        # arrange
        bind = self.BIND_UNDER_TEST(self.VALID_TRIGGER, self.VALID_COMMAND_LIST)
        # act
        is_empty = bind.is_empty()
        # assert
        assert is_empty is False


class TestWASDBind:
    def test_wasdbind_should_use_wasdtrigger_as_trigger_type(self):
        # arrange
        wasd_bind = WASDBind("W")
        # act
        trigger = wasd_bind.trigger
        wasd_bind.commands.add_toggle_on_power("super speed")
        # assert
        assert isinstance(trigger, _WASDTrigger)
        assert str(trigger) == "W"
        assert (
            str(wasd_bind) == 'W "+forward$$powexectoggleon super speed"'
        )  # No commands by default
