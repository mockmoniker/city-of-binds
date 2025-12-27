"""
Integration tests for WASDBindTemplate class.

These tests focus on WASDBindTemplate creation, modification, and build functionality
including WASD movement command injection and WASDBind object creation.
"""

import pytest

from CityOfBinds import WASDBind, WASDBindTemplate


class TestWASDBindTemplateCreation:
    """Test WASDBindTemplate object creation."""

    @pytest.fixture(params=["W", "A", "S", "D", "SPACE"])
    def wasd_key(self, request):
        """Fixture providing all valid WASD keys."""
        return request.param

    def test_basic_creation_all_keys(self, wasd_key):
        """Should create template with any valid WASD trigger."""
        template = WASDBindTemplate(wasd_key)
        assert template.trigger.key == wasd_key
        assert len(template.pools) == 0
        assert template.unique_count == 1

    def test_with_trigger_modifier(self):
        """Should create template with trigger modifier."""
        template = WASDBindTemplate("SHIFT+W")
        assert template.trigger.key == "W"
        assert template.trigger.modifier == "SHIFT"
