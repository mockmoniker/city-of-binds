import pytest
from CityOfBinds import Bind

valid_trigger_cases = [
    ("T", "T"),
    ("t", "T"),
    ("SPACE", "SPACE"),
    ("space", "SPACE"),
    ("SHIFT+T", "SHIFT+T"),
    ("shift+t", "SHIFT+T"),
    ("SHIFT+SPACE", "SHIFT+SPACE"),
    ("shift+space", "SHIFT+SPACE"),
]

class TestBindInitializaiton:
    @pytest.mark.parametrize("valid_trigger_input, expected_trigger_output", valid_trigger_cases)
    def test_bind_init_should_set_trigger_given_valid_trigger(self, valid_trigger_input, expected_trigger_output):
        bind = Bind(trigger=valid_trigger_input, slash_commands=["command"])
        assert bind.trigger == expected_trigger_output

    def test_bind_init_should_set_and_convert_lowercase_trigger(self):
        bind = Bind(trigger="trigger", slash_commands=["command"])
        assert bind.trigger == "TRIGGER"

    def test_bind_init_should_throw_error_invalid_trigger_given_invalid_trigger(self):
        with pytest.raises(ValueError):
            bind = Bind(trigger="trigger with space", slash_commands=["command"])

    def test_bind_init_should_set_slash_commands_given_single_command_as_str(self):
        bind = Bind(trigger="TRIGGER", slash_commands="command")
        assert bind.slash_commands == ["command"]

    def test_bind_init_should_set_slash_commands_given_single_command_as_list(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        assert bind.slash_commands == ["command"]

    def test_bind_init_should_set_slash_commands_given_multiple_commands(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command", "command2"])
        assert bind.slash_commands == ["command", "command2"]

    def test_bind_init_should_throw_error_empty_bind_given_empty_trigger(self):
        with pytest.raises(ValueError):
            bind = Bind(trigger="", slash_commands=["command"])

    def test_bind_init_should_throw_error_empty_bind_given_empty_slash_commands_as_str(self):
        with pytest.raises(ValueError):
            bind = Bind(trigger="TRIGGER", slash_commands="")

    def test_bind_init_should_throw_error_empty_bind_given_empty_slash_commands_as_list(self):
        with pytest.raises(ValueError):
            bind = Bind(trigger="TRIGGER", slash_commands=[])

class TestBindSetters:
    def test_bind_set_trigger_should_set_trigger_given_valid_trigger(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        bind.set_trigger("NEWTRIGGER")
        assert bind.trigger == "NEWTRIGGER"

    def test_bind_set_trigger_should_set_and_convert_lowercase_trigger(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        bind.set_trigger("newtrigger")
        assert bind.trigger == "NEWTRIGGER"

    def test_bind_set_trigger_should_throw_error_invalid_trigger_given_invalid_trigger(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        with pytest.raises(ValueError):
            bind.set_trigger("NEW TRIGGER WITH SPACE")

    def test_bind_set_slash_command_should_set_slash_command_given_single_command_as_str(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        bind.set_slash_command("newcommand")
        assert bind.slash_commands == ["newcommand"]

    def test_bind_set_slash_commands_should_set_slash_commands_given_single_command_as_str(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        bind.set_slash_commands("newcommand")
        assert bind.slash_commands == ["newcommand"]

    def test_bind_set_slash_commands_should_set_slash_commands_given_single_command_as_list(self):
        bind = Bind(trigger="TRIGGER", slash_commands=["command"])
        bind.set_slash_commands(["newcommand"])
        assert bind.slash_commands == ["newcommand"]