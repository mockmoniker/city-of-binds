import pytest
from CityOfBinds import Trigger

class TestValidTriggerInitialization:
    trigger_under_test = Trigger

    def test_init_should_set_trigger_key_given_valid_trigger_key(self):
        # arrange
        valid_trigger_key = 'W'
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_key)
        # assert
        assert trigger.trigger_key == valid_trigger_key

    def test_init_should_set_trigger_modifier_to_empty_string_given_trigger_key_only(self):
        # arrange
        valid_trigger_key = 'W'
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_key)
        # assert
        assert trigger.trigger_modifier == ''

    def test_init_should_set_capital_trigger_key_given_lowercase_trigger_key(self):
        # arrange
        lowercase_trigger_key = 'w'
        # act
        trigger = self.trigger_under_test(trigger_string=lowercase_trigger_key)
        # assert
        assert trigger.trigger_key == 'W'

    def test_init_should_set_modifier_given_valid_trigger_key_and_modifier(self):
        # arrange
        valid_trigger_key = "W"
        valid_trigger_modifier = "SHIFT"
        valid_trigger_string = f"{valid_trigger_modifier}+{valid_trigger_key}"
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_string)
        # assert
        assert trigger.trigger_modifier == "SHIFT"

    def test_init_should_set_capital_trigger_modifier_given_lowercase_trigger_modifier(self):
        # arrange
        valid_trigger_key = "w"
        lowercase_trigger_modifier = "shift"
        valid_trigger_string = f"{lowercase_trigger_modifier}+{valid_trigger_key}"
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_string)
        # assert
        assert trigger.trigger_modifier == "SHIFT"

class TestInvalidTriggerInitialization:
    trigger_under_test = Trigger

    def test_init_should_raise_value_error_given_empty_trigger_string(self):
        # arrange
        invalid_trigger_string = ''
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_trigger_string_with_spaces(self):
        # arrange
        invalid_trigger_string = 'SHIFT + W'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_trigger_string_with_multiple_modifiers(self):
        # arrange
        invalid_trigger_string = 'CTRL+SHIFT+W'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_trigger_string_with_empty_modifier(self):
        # arrange
        invalid_trigger_string = '+W'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_trigger_string_with_empty_key(self):
        # arrange
        invalid_trigger_string = 'SHIFT+'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

    def test_init_should_raise_value_error_given_trigger_string_with_multiple_plus_signs(self):
        # arrange
        invalid_trigger_string = 'SHIFT++W'
        # act
        with pytest.raises(ValueError) as excinfo:
            self.trigger_under_test(trigger_string=invalid_trigger_string)
        # assert
        assert "Invalid trigger format" in str(excinfo.value)

class TestValidTriggerSetters:
    trigger_under_test = Trigger

    def test_trigger_key_setter_should_set_trigger_key_given_valid_trigger_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        valid_trigger_key = "A"
        # act
        trigger.trigger_key = valid_trigger_key
        # assert
        assert trigger.trigger_key == valid_trigger_key
        assert trigger.trigger_modifier == ''

    def test_trigger_key_setter_should_set_capital_trigger_key_given_lowercase_trigger_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        lowercase_trigger_key = "a"
        # act
        trigger.trigger_key = lowercase_trigger_key
        # assert
        assert trigger.trigger_key == "A"
        assert trigger.trigger_modifier == ''

    def test_trigger_modifier_setter_should_set_trigger_modifier_given_valid_trigger_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        valid_trigger_modifier = "CTRL"
        # act
        trigger.trigger_modifier = valid_trigger_modifier
        # assert
        assert trigger.trigger_modifier == valid_trigger_modifier

    def test_trigger_modifier_setter_should_set_capital_trigger_modifier_given_lowercase_trigger_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        lowercase_trigger_modifier = "ctrl"
        # act
        trigger.trigger_modifier = lowercase_trigger_modifier
        # assert
        assert trigger.trigger_modifier == "CTRL"

    def test_trigger_modifier_setter_should_set_trigger_modifier_to_empty_string_given_empty_string(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="CTRL+W")
        valid_trigger_modifier = ''
        # act
        trigger.trigger_modifier = valid_trigger_modifier
        # assert
        assert trigger.trigger_modifier == valid_trigger_modifier

class TestInvalidTriggerSetters:
    trigger_under_test = Trigger

    def test_trigger_key_setter_should_raise_value_error_given_empty_trigger_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_trigger_key = ''
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.trigger_key = invalid_trigger_key
        # assert
        assert "Trigger key cannot be empty." in str(excinfo.value)

    def test_trigger_key_setter_should_raise_value_error_given_trigger_key_with_spaces(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_trigger_key = 'LEFT CLICK'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.trigger_key = invalid_trigger_key
        # assert
        assert "Trigger key cannot contain spaces." in str(excinfo.value)

    def test_trigger_key_setter_should_raise_value_error_given_invalid_trigger_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_trigger_key = 'WW'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.trigger_key = invalid_trigger_key
        # assert
        assert "for list of valid trigger keys." in str(excinfo.value)

    def test_trigger_modifier_setter_should_raise_value_error_given_trigger_modifier_with_spaces(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_trigger_modifier = 'LEFT SHIFT'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.trigger_modifier = invalid_trigger_modifier
        # assert
        assert "Trigger modifier cannot contain spaces." in str(excinfo.value)

    def test_trigger_modifier_setter_should_raise_value_error_given_invalid_trigger_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_trigger_modifier = 'CTRLL'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.trigger_modifier = invalid_trigger_modifier
        # assert
        assert "Invalid trigger modifier" in str(excinfo.value)

class TestTriggerStringProperty:
    trigger_under_test = Trigger

    def test_trigger_string_property_should_return_trigger_string_given_trigger_key_only(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        expected_trigger_string = "W"
        # act
        trigger_string = trigger.trigger_string
        # assert
        assert trigger_string == expected_trigger_string

    def test_trigger_string_property_should_return_trigger_string_given_trigger_key_and_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        expected_trigger_string = "SHIFT+W"
        # act
        trigger_string = trigger.trigger_string
        # assert
        assert trigger_string == expected_trigger_string

class TestTriggerMethods:
    trigger_under_test = Trigger

    def test_clear_modifier_should_set_trigger_modifier_to_empty_string(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        # act
        trigger.clear_modifier()
        # assert
        assert trigger.trigger_modifier == ''
        assert trigger.trigger_key == 'W'