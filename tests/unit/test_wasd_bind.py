"""
Unit tests for WASDBind class.

These tests focus on WASD-specific behavior while including minimal sanity checks
for basic bind functionality inherited from the base Bind class.
"""

import pytest

from CityOfBinds import WASDBind


class TestWASDBindCreation:
    """Test WASDBind object creation."""

    def test_trigger_only(self):
        """Should create bind with just a trigger."""
        bind = WASDBind("W")
        assert bind.trigger.key == "W"

    def test_with_trigger_modifier(self):
        """Should create bind with trigger and modifier."""
        bind = WASDBind("SHIFT+W")
        assert bind.trigger.key == "W"
        assert bind.trigger.modifier == "SHIFT"

    def test_trigger_and_single_command(self):
        """Should create bind with trigger and single command."""
        bind = WASDBind("W", ["powexectoggleon super speed"])
        assert bind.trigger.key == "W"
        assert len(bind.commands) == 1


class TestWASDBindRepresentation:
    """Test WASDBind representation."""

    def test_W_trigger_key(self):
        """Should return forward command."""
        bind = WASDBind("W")
        bind_str = str(bind)
        assert bind_str == 'W "+forward"'

    def test_A_trigger_key(self):
        """Should return left command."""
        bind = WASDBind("A")
        bind_str = str(bind)
        assert bind_str == 'A "+left"'

    def test_S_trigger_key(self):
        """Should return backward command."""
        bind = WASDBind("S")
        bind_str = str(bind)
        assert bind_str == 'S "+backward"'

    def test_D_trigger_key(self):
        """Should return right command."""
        bind = WASDBind("D")
        bind_str = str(bind)
        assert bind_str == 'D "+right"'

    def test_SPACE_trigger_key(self):
        """Should return up command."""
        bind = WASDBind("SPACE")
        bind_str = str(bind)
        assert bind_str == 'SPACE "+up"'

    def test_trigger_with_modifier(self):
        """Should return correct direction."""
        bind = WASDBind("SHIFT+W")
        bind_str = str(bind)
        assert bind_str == 'SHIFT+W "+forward"'

    def test_single_command_string_representation(self):
        """Should return correct string representation."""
        bind = WASDBind("W", ["powexectoggleon super speed"])
        bind_str = str(bind)
        assert bind_str == 'W "+forward$$powexectoggleon super speed"'

    def test_key_up_does_nothing(self):
        """Key-up trigger should not alter WASD command."""
        bind = WASDBind("W", ["powexectoggleon super speed"])
        bind.trigger_on_key_up = True
        bind_str = str(bind)
        assert bind_str == 'W "+forward$$powexectoggleon super speed"'


class TestWASDBindValidation:
    """Test WASDBind input validation."""

    @pytest.mark.parametrize("invalid_key", ["F", "Q", "E", "R", "T", "F1", "NUMPAD1"])
    def test_rejects_non_wasd_keys(self, invalid_key):
        """Should reject non-WASD keys."""
        with pytest.raises(ValueError, match="Unknown trigger key"):
            WASDBind(invalid_key)


class TestWASDBindComparison:
    """Test WASDBind comparisons."""

    def test_equal_binds_are_equal(self):
        """Binds with same trigger and commands should be equal."""
        bind1 = WASDBind("W", ["powexectoggleon super speed"])
        bind2 = WASDBind("W", ["powexectoggleon super speed"])
        assert bind1 == bind2

    def test_different_triggers_not_equal(self):
        """Binds with different triggers should not be equal."""
        bind1 = WASDBind("W")
        bind2 = WASDBind("S")
        assert bind1 != bind2

    def test_different_commands_not_equal(self):
        """Binds with different commands should not be equal."""
        bind1 = WASDBind("W", ["powexectoggleon super speed"])
        bind2 = WASDBind("W", ["powexectoggleon sprint"])
        assert bind1 != bind2
