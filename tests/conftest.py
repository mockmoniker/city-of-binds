"""
Shared fixtures for City of Binds test suite.

Provides common fixtures for unit tests, integration tests, and examples.
"""

import os
import pytest
from pathlib import Path
from CityOfBinds import Bind, WASDBind, BindFile, BindTemplate, RotatingBind


@pytest.fixture
def in_tmp_dir(tmp_path):
    """Fixture that changes working directory to tmp_path for the test duration."""
    og_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        yield tmp_path
    finally:
        os.chdir(og_cwd)


# === UNIT TEST FIXTURES ===


@pytest.fixture
def sample_trigger_strings():
    """Provides various trigger string samples for testing."""
    return [
        "W",
        "SPACE",
        "F1",
        "SHIFT+W",
        "CTRL+SPACE",
        "CTRL+SHIFT+F1",
        "ALT+TAB",
        "NUMPAD1",
    ]


@pytest.fixture
def sample_commands():
    """Provides various command samples for testing."""
    return [
        "forward",
        "+forward",
        "powexectoggleon super speed",
        "powexecname energy blast",
        'say "Hello World!"',
        "target_enemy_near",
        "bind w +forward",
    ]


@pytest.fixture
def sample_power_names():
    """Provides sample power names for testing."""
    return [
        "energy blast",
        "super speed",
        "flight",
        "dark nova",
        "granite armor",
        "hasten",
        "build up",
        "instant healing",
    ]


# === INTEGRATION TEST FIXTURES ===


@pytest.fixture
def basic_bind():
    """Creates a basic bind for testing."""
    return Bind("W", ["forward"])


@pytest.fixture
def wasd_bind():
    """Creates a WASD bind for testing."""
    return WASDBind("W", ["+forward"])


@pytest.fixture
def complex_bind():
    """Creates a complex bind with multiple commands."""
    return Bind(
        "SHIFT+Q",
        [
            "powexectoggleoff super speed",
            "powexecname energy blast",
            'team "Attacking!"',
            "powexectoggleon super speed",
        ],
    )


@pytest.fixture
def basic_bind_file():
    """Creates a basic bind file with common binds."""
    bind_file = BindFile()
    bind_file.add_bind(WASDBind("W", ["+forward"]))
    bind_file.add_bind(WASDBind("A", ["+left"]))
    bind_file.add_bind(WASDBind("S", ["+backward"]))
    bind_file.add_bind(WASDBind("D", ["+right"]))
    bind_file.add_bind(Bind("SPACE", ["+up"]))
    return bind_file


@pytest.fixture
def attack_bind_template():
    """Creates an attack bind template for testing."""
    return (
        BindTemplate("Q")
        .add_toggle_off_power("super speed")
        .add_power_pool(["energy blast", "power blast", "sniper blast"])
        .add_toggle_on_power("super speed")
    )


@pytest.fixture
def simple_rotating_bind(attack_bind_template):
    """Creates a simple rotating bind for testing."""
    return RotatingBind().add_bind_template(attack_bind_template)


# === EXAMPLE TEST FIXTURES ===


@pytest.fixture
def character_power_sets():
    """Provides sample character power sets for examples."""
    return {
        "blaster_primary": [
            "power bolt",
            "power blast",
            "power burst",
            "sniper blast",
            "energy torrent",
            "explosive blast",
            "nova",
        ],
        "blaster_secondary": [
            "power thrust",
            "energy punch",
            "bone smasher",
            "build up",
            "conserve power",
            "boost range",
            "total focus",
        ],
        "tank_primary": [
            "jab",
            "punch",
            "haymaker",
            "knockout blow",
            "hand clap",
            "foot stomp",
            "rage",
        ],
        "tank_secondary": [
            "temp invulnerability",
            "dull pain",
            "resist physical damage",
            "unyielding stance",
            "resist elements",
            "invincibility",
            "tough hide",
            "unstoppable",
        ],
    }


@pytest.fixture
def team_communication_messages():
    """Provides sample team communication messages."""
    return {
        "status": ["Ready!", "On my way!", "In position!", "Mission complete!"],
        "requests": ["Need help!", "Need healer!", "Need tank!", "Buff please!"],
        "tactical": ["Attack my target!", "Focus fire!", "Spread out!", "Group up!"],
        "emergency": ["RETREAT!", "INCOMING!", "HELP!", "MEDICAL!"],
    }


# === PERFORMANCE TEST FIXTURES ===


@pytest.fixture
def large_power_pool():
    """Creates a large power pool for performance testing."""
    return [f"test_power_{i}" for i in range(100)]


@pytest.fixture
def many_binds():
    """Creates many binds for performance testing."""
    binds = []
    for i in range(50):
        trigger = f"F{(i % 12) + 1}"
        if i >= 12:
            trigger = f"SHIFT+{trigger}"
        if i >= 24:
            trigger = f"CTRL+{trigger.replace('SHIFT+', '')}"
        binds.append(Bind(trigger, [f"test_command_{i}"]))
    return binds


# === VALIDATION TEST FIXTURES ===


@pytest.fixture
def invalid_triggers():
    """Provides invalid trigger strings for validation testing."""
    return [
        "",  # Empty
        "   ",  # Whitespace
        "INVALID+",  # Trailing plus
        "+W",  # Leading plus
        "CTRL++W",  # Double plus
        "BADKEY",  # Invalid key
        None,  # None value
    ]


@pytest.fixture
def invalid_commands():
    """Provides invalid command strings for validation testing."""
    return ["", "   ", None]  # Empty  # Whitespace only  # None value


# === FILE SYSTEM FIXTURES ===


@pytest.fixture
def sample_bind_files():
    """Creates sample bind files in tmp directory."""

    def _create_files(tmp_path):
        files = {}

        # Basic movement file
        movement = BindFile()
        movement.add_bind(WASDBind("W", ["+forward"]))
        movement.add_bind(WASDBind("S", ["+backward"]))
        files["movement.txt"] = movement

        # Attack file
        attacks = BindFile()
        attacks.add_bind(Bind("1", ["powexecname energy blast"]))
        attacks.add_bind(Bind("2", ["powexecname power blast"]))
        files["attacks.txt"] = attacks

        return files

    return _create_files


# === UTILITY FIXTURES ===


@pytest.fixture
def capture_file_operations(tmp_path):
    """Fixture to capture and verify file operations."""
    operations = []

    def capture_write(file_path, content):
        operations.append(
            {
                "operation": "write",
                "path": file_path,
                "content": content,
                "size": len(content),
            }
        )

    def capture_read(file_path):
        operations.append({"operation": "read", "path": file_path})

    return {
        "operations": operations,
        "capture_write": capture_write,
        "capture_read": capture_read,
    }


# === PYTEST CONFIGURATION ===


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line(
        "markers", "example: mark test as an example/end-to-end test"
    )
    config.addinivalue_line("markers", "performance: mark test as a performance test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
