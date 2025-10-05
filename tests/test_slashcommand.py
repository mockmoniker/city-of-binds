import pytest
from CityOfBinds import SlashCommand

class TestValidSlashCommandInitialization:
    action_under_test = SlashCommand

    def test_init_should_set_command_string_given_valid_slash_command_string(self):
        # arrange
        valid_slash_command_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.slash_command_string == 'powexectoggleon dark nova'

    def test_init_should_set_command_given_valid_slash_command_string(self):
        # arrange
        valid_slash_command_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.command == 'powexectoggleon'

    def test_init_should_set_args_given_valid_slash_command_string(self):
        # arrange
        valid_slash_command_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.args == 'dark nova'

    def test_init_should_set_command_string_given_uppercase_command(self):
        # arrange
        uppercase_command = 'POWEXECTOGGLEON dark nova'
        # act
        action = self.action_under_test(slash_command_string=uppercase_command)
        # assert
        assert action.slash_command_string == 'powexectoggleon dark nova'

    def test_init_should_set_command_given_uppercase_command(self):
        # arrange
        uppercase_command = 'POWEXECTOGGLEON dark nova'
        # act
        action = self.action_under_test(slash_command_string=uppercase_command)
        # assert
        assert action.command == 'powexectoggleon'

    def test_init_should_maintain_args_case_given_uppercase_args(self):
        # arrange
        uppercase_slash_command_string = 'POWEXECTOGGLEON DARK NOVA'
        # act
        action = self.action_under_test(slash_command_string=uppercase_slash_command_string)
        # assert
        assert action.args == 'DARK NOVA'

    def test_init_should_set_command_string_given_slash_command_string_with_no_args(self):
        # arrange
        valid_slash_command_string = 'forward'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.slash_command_string == 'forward'

    def test_init_should_set_command_given_slash_command_string_with_no_args(self):
        # arrange
        valid_slash_command_string = 'forward'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.command == 'forward'

    def test_init_should_set_args_to_empty_string_given_slash_command_string_with_no_args(self):
        # arrange
        valid_slash_command_string = 'forward'
        # act
        action = self.action_under_test(slash_command_string=valid_slash_command_string)
        # assert
        assert action.args == ''

class TestInvalidSlashCommandInitialization:
    action_under_test = SlashCommand

    def test_init_should_raise_value_error_given_empty_slash_command_string(self):
        # arrange
        invalid_slash_command_string = ''
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(slash_command_string=invalid_slash_command_string)
        # assert
        assert "Invalid slash command format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_slash_command_string_with_only_spaces(self):
        # arrange
        invalid_slash_command_string = '   '
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(slash_command_string=invalid_slash_command_string)
        # assert
        assert "Invalid slash command format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_slash_command_string_with_too_many_spaces(self):
        # arrange
        invalid_slash_command_string = 'powexectoggleon     dark nova'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(slash_command_string=invalid_slash_command_string)
        # assert
        assert "Invalid slash command format" in str(excinfo.value)




