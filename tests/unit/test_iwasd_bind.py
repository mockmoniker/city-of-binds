"""
Unit tests for iWASDBind class.

These tests focus on iWASD-specific behavior (inverted WASD movement) while including
minimal sanity checks for basic bind functionality inherited from the base classes.
"""

import pytest

from CityOfBinds import iWASDBind


class TestiWASDBindCreation:
    """Test iWASDBind object creation."""

    def test_trigger_only(self):
        """Should create bind with just a trigger."""
        bind = iWASDBind("W")
        assert bind.trigger.key == "W"

    def test_with_trigger_modifier(self):
        """Should create bind with trigger and modifier."""
        bind = iWASDBind("SHIFT+W")
        assert bind.trigger.key == "W"
        assert bind.trigger.modifier == "SHIFT"

    def test_trigger_and_single_command(self):
        """Should create bind with trigger and single command."""
        bind = iWASDBind("W", ["powexectoggleon super speed"])
        assert bind.trigger.key == "W"
        assert len(bind.commands) == 1


class TestiWASDBindRepresentation:
    """Test iWASDBind representation with inverted movement directions."""

    def test_W_trigger_key_inverted(self):
        """Should return backward command (inverted from forward)."""
        bind = iWASDBind("W")
        bind_str = str(bind)
        assert bind_str == 'W "+backward"'

    def test_A_trigger_key_inverted(self):
        """Should return right command (inverted from left)."""
        bind = iWASDBind("A")
        bind_str = str(bind)
        assert bind_str == 'A "+right"'

    def test_S_trigger_key_inverted(self):
        """Should return forward command (inverted from backward)."""
        bind = iWASDBind("S")
        bind_str = str(bind)
        assert bind_str == 'S "+forward"'

    def test_D_trigger_key_inverted(self):
        """Should return left command (inverted from right)."""
        bind = iWASDBind("D")
        bind_str = str(bind)
        assert bind_str == 'D "+left"'

    def test_SPACE_trigger_key_unchanged(self):
        """Should return up command (unchanged from WASD)."""
        bind = iWASDBind("SPACE")
        bind_str = str(bind)
        assert bind_str == 'SPACE "+up"'

    def test_trigger_with_modifier(self):
        """Should return correct inverted direction with modifier."""
        bind = iWASDBind("SHIFT+W")
        bind_str = str(bind)
        assert bind_str == 'SHIFT+W "+backward"'

    def test_single_command_string_representation(self):
        """Should return correct string representation with inverted movement."""
        bind = iWASDBind("W", ["powexectoggleon super speed"])
        bind_str = str(bind)
        assert bind_str == 'W "+backward$$powexectoggleon super speed"'

    def test_key_up_does_nothing(self):
        """Key-up trigger should not alter iWASD command."""
        bind = iWASDBind("W", ["powexectoggleon super speed"])
        bind.on_key_up = True
        bind_str = str(bind)
        assert bind_str == 'W "+backward$$powexectoggleon super speed"'


class TestiWASDBindValidation:
    """Test iWASDBind input validation (should inherit WASD validation)."""

    @pytest.mark.parametrize("invalid_key", ["F", "Q", "E", "R", "T", "F1", "NUMPAD1"])
    def test_rejects_non_wasd_keys(self, invalid_key):
        """Should reject non-WASD keys (same as WASDBind)."""
        with pytest.raises(ValueError, match="not allowed"):
            iWASDBind(invalid_key)


class TestiWASDBindComparison:
    """Test iWASDBind comparisons."""

    def test_equal_binds_are_equal(self):
        """Binds with same trigger and commands should be equal."""
        bind1 = iWASDBind("W", ["powexectoggleon super speed"])
        bind2 = iWASDBind("W", ["powexectoggleon super speed"])
        assert bind1 == bind2

    def test_different_triggers_not_equal(self):
        """Binds with different triggers should not be equal."""
        bind1 = iWASDBind("W")
        bind2 = iWASDBind("S")
        assert bind1 != bind2

    def test_different_commands_not_equal(self):
        """Binds with different commands should not be equal."""
        bind1 = iWASDBind("W", ["powexectoggleon super speed"])
        bind2 = iWASDBind("W", ["powexectoggleon sprint"])
        assert bind1 != bind2

    def test_iwasd_not_equal_to_wasd_same_trigger(self):
        """iWASDBind should not equal WASDBind even with same trigger (different movement)."""
        from CityOfBinds import WASDBind

        iwasd_bind = iWASDBind("W")
        wasd_bind = WASDBind("W")
        assert iwasd_bind != wasd_bind

    def test_iwasd_not_equal_to_wasd_with_commands(self):
        """iWASDBind should not equal WASDBind even with same trigger and commands."""
        from CityOfBinds import WASDBind

        iwasd_bind = iWASDBind("W", ["say test"])
        wasd_bind = WASDBind("W", ["say test"])
        assert iwasd_bind != wasd_bind
