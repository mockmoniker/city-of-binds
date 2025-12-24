"""
Integration tests for BindTemplate class.

These tests focus on BindTemplate creation, modification, and build functionality
including power pools and command generation.
"""

import pytest

from CityOfBinds import Bind, BindTemplate


class TestBindTemplateCreation:
    """Test BindTemplate object creation."""

    def test_basic_creation(self):
        """Should create template with just trigger."""
        template = BindTemplate("F1")
        assert template.trigger.key == "F1"
        assert len(template.pools) == 0
        assert template.unique_count == 1

    def test_with_trigger_modifier(self):
        """Should create template with trigger modifier."""
        template = BindTemplate("SHIFT+F1")
        assert template.trigger.key == "F1"
        assert template.trigger.modifier == "SHIFT"


class TestBindTemplateAddPools:
    """Test BindTemplate modification methods."""

    def test_add_power_pool(self):
        """Should add power pool to template."""
        template = BindTemplate("2")
        # act
        template.add_power_pool(["dark nova blast", "dark nova bolt"])
        # assert
        assert len(template.pools) == 1
        assert template.unique_count == 2  # Two powers

    def test_add_toggle_on_power_pool(self):
        """Should add toggle on power pool to template."""
        template = BindTemplate("W")
        # act
        template.add_toggle_on_power_pool(["super speed", "sprint"])
        # assert
        assert len(template.pools) == 1
        assert template.unique_count == 2  # Two toggle on powers

    def test_add_toggle_off_power_pool(self):
        """Should add toggle off power pool to template."""
        template = BindTemplate("W")
        # act
        template.add_toggle_off_power_pool(["dark nova", "black dwarf"])
        # assert
        assert len(template.pools) == 1
        assert template.unique_count == 2  # Two toggle off powers

    def test_add_auto_power_pool(self):
        """Should add auto power pool to template."""
        template = BindTemplate("W")
        # act
        template.add_auto_power_pool(["hasten", "inner inspiration"])
        # assert
        assert len(template.pools) == 1
        assert template.unique_count == 2  # Two auto powers

    def test_add_command_arguments_pool(self):
        """Should add custom command arguments pool."""
        template = BindTemplate("F1")
        # act
        template.add_command_arguments_pool("say", ["hello", "goodbye"])
        # assert
        assert len(template.pools) == 1
        assert template.unique_count == 2

    def test_add_multiple_power_pools(self):
        """Should add multiple power pools to template."""
        template = BindTemplate("W")
        # act
        template.add_auto_power_pool(["hasten", "inner inspiration"])
        template.add_toggle_on_power_pool(["super speed", "sprint"])
        # assert
        assert len(template.pools) == 2
        assert template.unique_count == 2

    def test_chaining_pool_methods(self):
        """Should support method chaining."""
        template = BindTemplate("4")
        # act
        (
            template.add_toggle_off_power_pool(["dark nova"])
            .add_toggle_off_power_pool(["black dwarf"])
            .add_power_pool(["sunless mire", "quasar"])
            .add_auto_power_pool(["hasten", "inner inspiration"])
        )
        # assert
        assert len(template.pools) == 4
        assert template.unique_count == 2


class TestBindTemplateBuildSingle:
    """Test BindTemplate single bind building."""

    def test_build_bind_with_power_pool(self):
        """Should build bind with power from pool."""
        template = BindTemplate("2")
        template.add_power_pool(["dark nova blast", "dark nova bolt"])

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == '2 "powexecname dark nova blast"'

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == '2 "powexecname dark nova bolt"'

    def test_build_bind_with_toggle_on_power_pool(self):
        """Should build bind with toggle on power from pool."""
        template = BindTemplate("W")
        template.add_toggle_on_power_pool(["super speed", "sprint"])

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == 'W "powexectoggleon super speed"'

        # act
        bind = template.build()
        bind_str = str(bind)
        # assert
        assert bind_str == 'W "powexectoggleon sprint"'

    def test_build_bind_with_toggle_off_power_pool(self):
        """Should build bind with toggle off power from pool."""
        template = BindTemplate("W")
        template.add_toggle_off_power_pool(["dark nova", "black dwarf"])

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == 'W "powexectoggleoff dark nova"'

        # act
        bind = template.build()
        bind_str = str(bind)
        # assert
        assert bind_str == 'W "powexectoggleoff black dwarf"'

    def test_build_bind_with_auto_power_pool(self):
        """Should build bind with auto power from pool."""
        template = BindTemplate("W")
        template.add_auto_power_pool(["hasten", "inner inspiration"])

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == 'W "powexecauto hasten"'

        # act
        bind = template.build()
        bind_str = str(bind)
        # assert
        assert bind_str == 'W "powexecauto inner inspiration"'

    def test_build_bind_with_command_arguments_pool(self):
        """Should build bind with command arguments from pool."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["hello", "goodbye"])

        # act
        bind = template.build()
        # assert
        assert isinstance(bind, Bind)
        bind_str = str(bind)
        assert bind_str == 'F1 "say hello"'

        # act
        bind = template.build()
        bind_str = str(bind)
        # assert
        assert bind_str == 'F1 "say goodbye"'

    def test_build_rolls_over(self):
        """Should roll over pools when building more than unique count."""
        template = BindTemplate("2")
        template.add_power_pool(["dark nova blast", "dark nova bolt"])

        # act & assert
        bind = template.build()
        assert str(bind) == '2 "powexecname dark nova blast"'

        bind = template.build()
        assert str(bind) == '2 "powexecname dark nova bolt"'

        # Should roll over to first power again
        bind = template.build()
        assert str(bind) == '2 "powexecname dark nova blast"'


class TestBindTemplateBuildMultiple:
    """Test BindTemplate multiple bind building."""

    def test_build_multiple(self):
        """Should build specified number of binds."""
        template = BindTemplate("2")
        template.add_power_pool(
            ["dark nova blast", "dark nova bolt", "dark nova detonation"]
        )
        # act
        binds = template.build(3)
        # assert
        assert isinstance(binds, list)
        assert len(binds) == 3
        assert all(isinstance(bind, Bind) for bind in binds)
        assert str(binds[0]) == '2 "powexecname dark nova blast"'
        assert str(binds[1]) == '2 "powexecname dark nova bolt"'
        assert str(binds[2]) == '2 "powexecname dark nova detonation"'

    def test_build_all(self):
        """Should build all unique combinations."""
        template = BindTemplate("2")
        template.add_power_pool(["dark nova blast", "dark nova bolt"])
        template.add_command_arguments_pool(
            "say", ["take that!", "and that!", "and a little of this!"]
        )
        # act
        b = template.build_all()
        # assert
        assert isinstance(b, list)
        assert len(b) == 6  # 2 powers * 3 sayings = 6 combinations
        assert all(isinstance(bind, Bind) for bind in b)
        assert str(b[0]) == '2 "powexecname dark nova blast$$say take that!"'
        assert str(b[1]) == '2 "powexecname dark nova bolt$$say and that!"'
        assert str(b[2]) == '2 "powexecname dark nova blast$$say and a little of this!"'
        assert str(b[3]) == '2 "powexecname dark nova bolt$$say take that!"'
        assert str(b[4]) == '2 "powexecname dark nova blast$$say and that!"'
        assert str(b[5]) == '2 "powexecname dark nova bolt$$say and a little of this!"'

    def test_build_sets(self):
        """Should build multiple sets of all combinations."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["hey", "hi", "how are ya"])
        # act
        binds = template.build_sets(2)  # 2 sets
        # assert
        assert isinstance(binds, list)
        assert len(binds) == 6  # 3 sayings * 2 sets = 6 binds
        assert all(isinstance(bind, Bind) for bind in binds)
        assert str(binds[0]) == 'F1 "say hey"'
        assert str(binds[1]) == 'F1 "say hi"'
        assert str(binds[2]) == 'F1 "say how are ya"'
        assert str(binds[3]) == 'F1 "say hey"'
        assert str(binds[4]) == 'F1 "say hi"'
        assert str(binds[5]) == 'F1 "say how are ya"'


class TestBindTemplateUniqueCount:
    """Test BindTemplate unique count calculations."""

    def test_unique_count_no_pools(self):
        """Should return 1 for no pools."""
        template = BindTemplate("F1")
        assert template.unique_count == 1

    def test_unique_count_single_pool(self):
        """Should return pool size for single pool."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["hey", "hi", "how are ya"])
        assert template.unique_count == 3

    def test_unique_count_multiple_pools_same_size(self):
        """Should return product for pools of same size."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["hello", "hi"])  # 2
        template.add_command_arguments_pool("e", ["wave", "dance"])  # 2
        assert template.unique_count == 2  # LCM(2, 2) = 2

    def test_unique_count_multiple_pools_different_sizes(self):
        """Should return LCM for pools of different sizes."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["hello", "hey", "how are ya"])  # 3
        template.add_command_arguments_pool("e", ["wave", "dance"])  # 2
        assert template.unique_count == 6  # LCM(3, 2) = 6

    def test_unique_count_lcm_calculation(self):
        """Should correctly calculate LCM for complex cases."""
        template = BindTemplate("F1")
        template.add_command_arguments_pool("say", ["a", "b", "c", "d"])  # 4
        template.add_command_arguments_pool("say", ["x", "y", "z", "w", "v", "u"])  # 6
        assert template.unique_count == 12  # LCM(4, 6) = 12
