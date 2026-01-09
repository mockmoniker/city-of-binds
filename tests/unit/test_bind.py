"""
Unit tests for Bind class.

These tests focus on individual Bind creation, modification, representation, validation, and class utils.
"""

import pytest

from CityOfBinds import Bind
from CityOfBinds.src._configs.constants import GameConstants


class TestBindCreation:
    """Test Bind object creation."""

    def test_trigger_only(self):
        """Should create bind with just a trigger."""
        bind = Bind("Q")
        assert bind.trigger.key == "Q"

    def test_multi_char_trigger_key(self):
        """Should create bind with multi-character trigger key."""
        bind = Bind("SPACE")
        assert bind.trigger.key == "SPACE"

    def test_empty_commands(self):
        """Should create bind with empty commands list."""
        bind = Bind("Q", [])
        assert bind.trigger.key == "Q"
        assert len(bind.commands) == 0

    def test_none_commands(self):
        """Should create bind with None commands as empty list."""
        bind = Bind("Q", None)
        assert bind.trigger.key == "Q"
        assert len(bind.commands) == 0

    def test_trigger_and_single_command(self):
        """Should create bind with trigger and single command."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        assert bind.trigger.key == "Q"
        assert len(bind.commands) == 1

    def test_trigger_and_multiple_commands(self):
        """Should create bind with trigger and multiple commands."""
        commands = ["powexectoggleoff black dwarf", "powexectoggleon dark nova"]
        bind = Bind("Q", commands)
        assert bind.trigger.key == "Q"
        assert len(bind.commands) == 2

    def test_with_trigger_modifier(self):
        """Should handle triggers with modifiers."""
        bind = Bind("SHIFT+Q", ["powexectoggleoff dark nova"])
        assert bind.trigger.key == "Q"
        assert bind.trigger.modifier == "SHIFT"


class TestBindTriggerModification:
    """Test Bind trigger modification."""

    def test_modify_trigger(self):
        """Should allow modifying the trigger after creation."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        # act
        bind.trigger = "SHIFT+SPACE"
        # assert
        assert bind.trigger.key == "SPACE"
        assert bind.trigger.modifier == "SHIFT"

    def test_modify_trigger_key(self):
        """Should allow modifying the trigger key after creation."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        # act
        bind.trigger.key = "E"
        # assert
        assert bind.trigger.key == "E"

    def test_add_trigger_modifier(self):
        """Should allow adding the trigger modifier after creation."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        # act
        bind.trigger.modifier = "CTRL"
        # assert
        assert bind.trigger.key == "Q"
        assert bind.trigger.modifier == "CTRL"

    def test_modify_trigger_modifier(self):
        """Should allow modifying the trigger modifier after creation."""
        bind = Bind("SHIFT+Q", ["powexectoggleon dark nova"])
        # act
        bind.trigger.modifier = "CTRL"
        # assert
        assert bind.trigger.key == "Q"
        assert bind.trigger.modifier == "CTRL"

    def test_remove_trigger_modifier(self):
        """Should allow removing the trigger modifier after creation."""
        bind = Bind("SHIFT+Q", ["powexectoggleon dark nova"])
        # act
        bind.trigger.modifier = None
        # assert
        assert bind.trigger.key == "Q"
        assert bind.trigger.modifier is ""


class TestBindCommandsModification:
    """Test Bind command modification."""

    def test_add_command(self):
        """Should allow adding commands after creation."""
        bind = Bind("Q")
        # act
        bind.commands.add_command("powexectoggleon dark nova")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexectoggleon dark nova"

    def test_add_power(self):
        """Should allow adding a powexecname command for a power."""
        bind = Bind("Q")
        # act
        bind.commands.add_power("dark nova")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexecname dark nova"

    def test_add_toggleon_power(self):
        """Should allow adding a powexectoggleon command for a power."""
        bind = Bind("Q")
        # act
        bind.commands.add_toggle_on_power("dark nova")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexectoggleon dark nova"

    def test_add_toggleoff_power(self):
        """Should allow adding a powexectoggleoff command for a power."""
        bind = Bind("Q")
        # act
        bind.commands.add_toggle_off_power("dark nova")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexectoggleoff dark nova"

    def test_add_auto_power(self):
        """Should allow adding a powexecauto command for a power."""
        bind = Bind("H")
        # act
        bind.commands.add_auto_power("hasten")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexecauto hasten"

    def test_add_loc_self_power(self):
        """Should allow adding a powexecloc self command for a power."""
        bind = Bind("5")
        # act
        bind.commands.add_loc_self_power("rain of fire")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexeclocation me rain of fire"

    def test_add_loc_target_power(self):
        """Should allow adding a powexecloc target command for a power."""
        bind = Bind("5")
        # act
        bind.commands.add_loc_target_power("rain of fire")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexeclocation target rain of fire"

    def test_add_loc_cursor_power(self):
        """Should allow adding a powexecloc cursor command for a power."""
        bind = Bind("5")
        # act
        bind.commands.add_loc_cursor_power("rain of fire")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "powexeclocation cursor rain of fire"

    def test_add_movement(self):
        """Should allow adding movement commands."""
        bind = Bind("W")
        # act
        bind.commands.add_movement("forward")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "+forward"

        bind = Bind("A")
        # act
        bind.commands.add_movement("left")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "+left"

        bind = Bind("S")
        # act
        bind.commands.add_movement("backward")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "+backward"

        bind = Bind("D")
        # act
        bind.commands.add_movement("right")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "+right"

        bind = Bind("SPACE")
        # act
        bind.commands.add_movement("up")
        # assert
        assert len(bind.commands) == 1
        assert bind.commands[0] == "+up"

    def test_chain_multiple_commands(self):
        """Should allow chaining multiple command additions."""
        bind = Bind("Q")
        # act
        (
            bind.commands.add_toggle_off_power("black dwarf")
            .add_toggle_on_power("dark nova")
            .add_auto_power("dark nova blast")
        )
        # assert
        assert len(bind.commands) == 3
        assert bind.commands[0] == "powexectoggleoff black dwarf"
        assert bind.commands[1] == "powexectoggleon dark nova"
        assert bind.commands[2] == "powexecauto dark nova blast"

    def test_insert_commands_at_index(self):
        """Should allow inserting commands at specific indices."""
        bind = Bind("F1", ["say hi", "say hello", "say konichiwa"])
        # act
        bind.commands.add_command("say aloha", index=1)
        bind.commands.add_command("say bonjour", index=-1)
        bind.commands.add_command("say hola", index=999)
        # assert
        assert len(bind.commands) == 6
        assert bind.commands[0] == "say hi"
        assert bind.commands[1] == "say aloha"
        assert bind.commands[2] == "say hello"
        assert bind.commands[3] == "say bonjour"
        assert bind.commands[4] == "say konichiwa"
        assert bind.commands[5] == "say hola"


class TestBindRepresentation:
    """Test Bind representation."""

    def test_trigger_modifier_string_representation(self):
        """Should return correct string representation."""
        bind = Bind("SHIFT+Q", ["powexectoggleoff dark nova"])
        bind_str = str(bind)
        assert bind_str == 'SHIFT+Q "powexectoggleoff dark nova"'

    def test_single_command_string_representation(self):
        """Should return correct string representation."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bind_str = str(bind)
        assert bind_str == 'Q "powexectoggleon dark nova"'

    def test_multi_command_string_representation(self):
        """Should return correct string representation."""
        bind = Bind(
            "Q",
            [
                "powexectoggleoff black dwarf",
                "powexectoggleon dark nova",
                "powexecauto dark nova blast",
            ],
        )
        bind_str = str(bind)
        assert (
            bind_str
            == 'Q "powexectoggleoff black dwarf$$powexectoggleon dark nova$$powexecauto dark nova blast"'
        )

    def test_key_up_trigger_string_representation(self):
        """Should return correct string representation for key-up trigger."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        bind.on_key_up = True
        bind_str = str(bind)
        assert bind_str == 'Q "+$$powexectoggleon dark nova"'


class TestBindValidation:
    """Test Bind input validation."""

    def test_is_empty_true(self):
        """Should return True for empty bind."""
        bind = Bind("Q")
        assert bind.is_empty() is True

    def test_is_empty_false(self):
        """Should return False for non-empty bind."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        assert bind.is_empty() is False

    # TODO: narrow these tests once bind length is validted in game (2025/12/22)
    def test_is_over_bind_length_true(self):
        """Should return True for bind within max length."""
        long_command = "l " + "A" * (GameConstants.MAX_BIND_LENGTH + 50)
        bind = Bind("Q", [long_command])
        assert bind.is_over_bind_length() is True

    def test_is_over_bind_length_false(self):
        """Should return False for bind exceeding max length."""
        short_command = "l " + "A" * (GameConstants.MAX_BIND_LENGTH - 50)
        bind = Bind("Q", [short_command])
        assert bind.is_over_bind_length() is False

    def test_is_valid_true(self):
        """Should return True for valid bind."""
        bind = Bind("Q", ["powexectoggleon dark nova"])
        assert bind.is_valid() is True

    def test_is_valid_false_empty(self):
        """Should return False for invalid (empty) bind."""
        bind = Bind("Q")
        assert bind.is_valid() is False

    def test_is_valid_false_exceeds_length(self):
        """Should return False for invalid (exceeds length) bind."""
        short_command = "l " + "A" * (GameConstants.MAX_BIND_LENGTH + 50)
        bind = Bind("Q", [short_command])
        assert bind.is_valid() is False


class TestBindComparison:
    """Test Bind comparisons."""

    def test_equal_binds_are_equal(self):
        """Binds with same trigger and commands should be equal."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("Q", ["powexectoggleon dark nova"])
        assert bind1 == bind2

    def test_different_triggers_not_equal(self):
        """Binds with different triggers should not be equal."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("E", ["powexectoggleon dark nova"])
        assert bind1 != bind2

    def test_different_commands_not_equal(self):
        """Binds with different commands should not be equal."""
        bind1 = Bind("Q", ["powexectoggleon dark nova"])
        bind2 = Bind("Q", ["powexectoggleon black dwarf"])
        assert bind1 != bind2
