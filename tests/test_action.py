import pytest
from CityOfBinds import Action

class TestValidActionInitialization:
    action_under_test = Action

    def test_init_should_set_action_string_given_valid_action_string(self):
        # arrange
        valid_action_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.action_string == 'powexectoggleon dark nova'

    def test_init_should_set_slash_command_given_valid_action_string(self):
        # arrange
        valid_action_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.slash_command == 'powexectoggleon'

    def test_init_should_set_args_given_valid_action_string(self):
        # arrange
        valid_action_string = 'powexectoggleon dark nova'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.args == 'dark nova'

    def test_init_should_set_action_string_given_uppercase_action_string(self):
        # arrange
        uppercase_action_string = 'POWEXECTOGGLEON DARK NOVA'
        # act
        action = self.action_under_test(action_string=uppercase_action_string)
        # assert
        assert action.action_string == 'powexectoggleon dark nova'
    
    def test_init_should_set_slash_command_given_uppercase_action_string(self):
        # arrange
        uppercase_action_string = 'POWEXECTOGGLEON DARK NOVA'
        # act
        action = self.action_under_test(action_string=uppercase_action_string)
        # assert
        assert action.slash_command == 'powexectoggleon'

    def test_init_should_set_args_given_uppercase_action_string(self):
        # arrange
        uppercase_action_string = 'POWEXECTOGGLEON DARK NOVA'
        # act
        action = self.action_under_test(action_string=uppercase_action_string)
        # assert
        assert action.args == 'dark nova'

    def test_init_should_set_action_string_given_action_string_with_no_args(self):
        # arrange
        valid_action_string = 'forward'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.action_string == 'forward'

    def test_init_should_set_slash_command_given_action_string_with_no_args(self):
        # arrange
        valid_action_string = 'forward'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.slash_command == 'forward'

    def test_init_should_set_args_to_empty_string_given_action_string_with_no_args(self):
        # arrange
        valid_action_string = 'forward'
        # act
        action = self.action_under_test(action_string=valid_action_string)
        # assert
        assert action.args == ''

class TestInvalidActionInitialization:
    action_under_test = Action

    def test_init_should_raise_value_error_given_empty_action_string(self):
        # arrange
        invalid_action_string = ''
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(action_string=invalid_action_string)
        # assert
        assert "Invalid action format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_action_string_with_only_spaces(self):
        # arrange
        invalid_action_string = '   '
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(action_string=invalid_action_string)
        # assert
        assert "Invalid action format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_action_string_with_too_many_spaces(self):
        # arrange
        invalid_action_string = 'powexectoggleon     dark nova'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.action_under_test(action_string=invalid_action_string)
        # assert
        assert "Invalid action format" in str(excinfo.value)




