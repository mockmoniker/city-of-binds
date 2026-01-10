"""
Unit tests for Macro class.

These tests focus on individual Macro creation, modification, representation, and string generation.
"""

import pytest

from CityOfBinds import CommandGroup, Macro
from CityOfBinds.src._configs.constants import MacroCommands


class TestMacroCreation:
    """Test Macro object creation."""

    def test_name_only(self):
        """Should create macro with just a name."""
        macro = Macro("test_macro")
        assert macro.name == "test_macro"
        assert len(macro.commands) == 0

    def test_name_with_empty_commands(self):
        """Should create macro with empty commands list."""
        macro = Macro("test_macro", [])
        assert macro.name == "test_macro"
        assert len(macro.commands) == 0

    def test_name_with_none_commands(self):
        """Should create macro with None commands as empty list."""
        macro = Macro("test_macro", None)
        assert macro.name == "test_macro"
        assert len(macro.commands) == 0

    def test_name_with_single_command(self):
        """Should create macro with name and single command."""
        macro = Macro("heal_macro", ["powexecname heal"])
        assert macro.name == "heal_macro"
        assert len(macro.commands) == 1

    def test_name_with_multiple_commands(self):
        """Should create macro with name and multiple commands."""
        commands = ["powexecname heal", "say Healing!"]
        macro = Macro("heal_macro", commands)
        assert macro.name == "heal_macro"
        assert len(macro.commands) == 2


class TestMacroStringGeneration:
    """Test Macro string generation methods."""

    def test_macro_string_name_only(self):
        """Should generate macro string with name only."""
        macro = Macro("test_macro")
        result = macro.get_str()
        expected = f'{MacroCommands.MACRO} "test_macro" {macro.commands}'
        assert result == expected

    def test_macro_string_with_commands(self):
        """Should generate macro string with name and commands."""
        commands = ["powexecname heal", "say Healing!"]
        macro = Macro("heal_macro", commands)
        result = macro.get_str()
        expected = f'{MacroCommands.MACRO} "heal_macro" {macro.commands}'
        assert result == expected

    def test_str_representation(self):
        """Should return macro string when converted to string."""
        macro = Macro("test_macro", ["say hello"])
        result = str(macro)
        expected = macro.get_str()
        assert result == expected


class TestMacroCommandsHandling:
    """Test Macro commands property handling via CommandsMixin."""

    def test_commands_property_returns_command_group(self):
        """Should return commands as CommandGroup instance."""
        commands = ["powexecname heal", "say Healing!"]
        macro = Macro("heal_macro", commands)
        assert isinstance(macro.commands, CommandGroup)

    def test_set_commands_with_list(self):
        """Should allow setting commands with a list."""
        macro = Macro("test_macro")
        new_commands = ["powexecname heal", "say Healing!"]
        # act
        macro.commands = new_commands
        # assert
        assert len(macro.commands) == 2

    def test_set_commands_with_command_group(self):
        """Should allow setting commands with a CommandGroup."""
        macro = Macro("test_macro")
        command_group = CommandGroup(["powexecname heal", "say Healing!"])
        # act
        macro.commands = command_group
        # assert
        assert len(macro.commands) == 2
        # Should be a deep copy, not the same instance
        assert macro.commands is not command_group

    def test_set_commands_invalid_type_raises_error(self):
        """Should raise TypeError when setting commands with invalid type."""
        macro = Macro("test_macro")
        with pytest.raises(TypeError, match="Invalid type.*Commands must be set using"):
            macro.commands = "invalid"

    def test_modify_commands_after_creation(self):
        """Should allow modifying commands after creation."""
        macro = Macro("test_macro", ["e dance"])
        # act
        macro.commands = ["e popdance", "l hi"]
        # assert
        assert len(macro.commands) == 2


class TestMacroConstants:
    """Test Macro class constants."""

    def test_macro_command_constant(self):
        """Should have correct MACRO_COMMAND constant."""
        assert Macro.MACRO_COMMAND == MacroCommands.MACRO
        assert Macro.MACRO_COMMAND == "macro"


class TestMacroIntegration:
    """Test Macro integration scenarios."""

    def test_empty_macro_string_generation(self):
        """Should generate valid macro string even with no commands."""
        macro = Macro("empty_macro")
        result = macro.get_str()
        # Should contain the macro command and name at minimum
        assert MacroCommands.MACRO in result
        assert "empty_macro" in result

    def test_complex_macro_scenario(self):
        """Should handle complex macro with multiple commands."""
        commands = [
            "powexecname heal",
            "say Casting heal!",
            "emote point",
            "tell $target, Healing you!",
        ]
        macro = Macro("complex_heal", commands)

        # Test all aspects work together
        assert macro.name == "complex_heal"
        assert len(macro.commands) == 4

        macro_string = str(macro)
        assert MacroCommands.MACRO in macro_string
        assert "complex_heal" in macro_string

    def test_macro_name_modification(self):
        """Should allow modifying macro name after creation."""
        macro = Macro("original_name", ["say hello"])
        # act
        macro.name = "new_name"
        # assert
        assert macro.name == "new_name"
        # String representation should reflect the change
        macro_string = str(macro)
        assert "new_name" in macro_string
        assert "original_name" not in macro_string
