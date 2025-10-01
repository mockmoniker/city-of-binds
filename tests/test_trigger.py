import pytest
from CityOfBinds import Trigger

class TestValidTriggerInitialization:
    trigger_under_test = Trigger

    def test_init_should_set_key_given_valid_key(self):
        # arrange
        valid_key = 'W'
        # act
        trigger = self.trigger_under_test(trigger_string=valid_key)
        # assert
        assert trigger.key == 'W'

    def test_init_should_set_modifier_to_empty_string_given_key_only(self):
        # arrange
        valid_key = 'W'
        # act
        trigger = self.trigger_under_test(trigger_string=valid_key)
        # assert
        assert trigger.modifier == ''

    def test_init_should_set_capital_key_given_lowercase_key(self):
        # arrange
        lowercase_key = 'w'
        # act
        trigger = self.trigger_under_test(trigger_string=lowercase_key)
        # assert
        assert trigger.key == 'W'

    def test_init_should_set_modifier_given_valid_key_and_modifier(self):
        # arrange
        valid_key = "W"
        valid_modifier = "SHIFT"
        valid_trigger_string = f"{valid_modifier}+{valid_key}"
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_string)
        # assert
        assert trigger.modifier == "SHIFT"

    def test_init_should_set_capital_modifier_given_lowercase_modifier(self):
        # arrange
        valid_key = "w"
        lowercase_modifier = "shift"
        valid_trigger_string = f"{lowercase_modifier}+{valid_key}"
        # act
        trigger = self.trigger_under_test(trigger_string=valid_trigger_string)
        # assert
        assert trigger.modifier == "SHIFT"

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

    def test_key_setter_should_set_key_given_valid_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        valid_key = "A"
        # act
        trigger.key = valid_key
        # assert
        assert trigger.key == valid_key
        assert trigger.modifier == ''

    def test_key_setter_should_set_capital_key_given_lowercase_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        lowercase_key = "a"
        # act
        trigger.key = lowercase_key
        # assert
        assert trigger.key == "A"

    def test_modifier_setter_should_set_modifier_given_valid_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        valid_modifier = "CTRL"
        # act
        trigger.modifier = valid_modifier
        # assert
        assert trigger.modifier == valid_modifier

    def test_modifier_setter_should_set_capital_modifier_given_lowercase_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        lowercase_modifier = "ctrl"
        # act
        trigger.modifier = lowercase_modifier
        # assert
        assert trigger.modifier == "CTRL"

    def test_modifier_setter_should_set_modifier_to_empty_string_given_empty_string(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="CTRL+W")
        valid_modifier = ''
        # act
        trigger.modifier = valid_modifier
        # assert
        assert trigger.modifier == valid_modifier

class TestInvalidTriggerSetters:
    trigger_under_test = Trigger

    def test_key_setter_should_raise_value_error_given_empty_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_key = ''
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.key = invalid_key
        # assert
        assert "Trigger key cannot be empty." in str(excinfo.value)

    def test_key_setter_should_raise_value_error_given_key_with_spaces(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_key = 'LEFT CLICK'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.key = invalid_key
        # assert
        assert "Trigger key cannot contain spaces." in str(excinfo.value)

    def test_key_setter_should_raise_value_error_given_invalid_key(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_key = 'WW'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.key = invalid_key
        # assert
        assert "for list of valid trigger keys." in str(excinfo.value)

    def test_modifier_setter_should_raise_value_error_given_modifier_with_spaces(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_modifier = 'LEFT SHIFT'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.modifier = invalid_modifier
        # assert
        assert "Trigger modifier cannot contain spaces." in str(excinfo.value)

    def test_modifier_setter_should_raise_value_error_given_invalid_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        invalid_modifier = 'CTRLL'
        # act
        with pytest.raises(ValueError) as excinfo:
            trigger.modifier = invalid_modifier
        # assert
        assert "Invalid trigger modifier" in str(excinfo.value)

class TestTriggerStringProperty:
    trigger_under_test = Trigger

    def test_trigger_string_property_should_return_trigger_string_given_key_only(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="W")
        expected_trigger_string = "W"
        # act
        trigger_string = trigger.trigger_string
        # assert
        assert trigger_string == expected_trigger_string

    def test_trigger_string_property_should_return_trigger_string_given_key_and_modifier(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        expected_trigger_string = "SHIFT+W"
        # act
        trigger_string = trigger.trigger_string
        # assert
        assert trigger_string == expected_trigger_string

class TestTriggerMethods:
    trigger_under_test = Trigger

    def test_clear_modifier_should_set_modifier_to_empty_string(self):
        # arrange
        trigger = self.trigger_under_test(trigger_string="SHIFT+W")
        # act
        trigger.clear_modifier()
        # assert
        assert trigger.modifier == ''
        assert trigger.key == 'W'