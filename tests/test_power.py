import pytest
from CityOfBinds.src.game.utils.powers import _Power


class TestInitialization:
    # region Valid Initialization Tests

    def test_init_should_accept_single_word_power_string(self):
        # arrange
        power_string = "hasten"
        # act
        power = _Power(power_string)
        # assert
        assert str(power) == "hasten"

    def test_init_should_accept_multi_word_power_string(self):
        # arrange
        power_string = "super speed"
        # act
        power = _Power(power_string)
        # assert
        assert str(power) == "super speed"

    def test_init_should_accept_uppercase_power_string(self):
        # arrange
        power_string = "SUPER SPEED"
        # act
        power = _Power(power_string)
        # assert
        assert str(power) == "super speed"

    # endregion

    # region Invalid Initialization Tests

    def test_init_should_throw_error_given_empty_power_string(self):
        # arrange
        power_string = ""
        # act
        with pytest.raises(ValueError) as excinfo:
            _Power(power_string)
        # assert
        assert "Invalid power format" in str(excinfo.value)

    def test_init_should_throw_error_given_power_string_with_numbers(self):
        # arrange
        power_string = "speed123"
        # act
        with pytest.raises(ValueError) as excinfo:
            _Power(power_string)
        # assert
        assert "Invalid power format" in str(excinfo.value)

    def test_init_should_throw_error_given_power_string_with_special_characters(self):
        # arrange
        power_string = "super-speed!"
        # act
        with pytest.raises(ValueError) as excinfo:
            _Power(power_string)
        # assert
        assert "Invalid power format" in str(excinfo.value)

    # endregion
