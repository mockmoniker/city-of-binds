#!/usr/bin/env python3
"""
Generate valid_commands.py directly from JSON data
"""

import json
from pathlib import Path
from datetime import datetime, timezone


COMMENT_BANNER = f'''"""
DO NOT EDIT - Run scripts/{Path(__file__).name} to regenerate

Generated: {{timestamp}}
"""'''


def get_files():
    root = Path(__file__).parent.parent
    input_file = root / "resources" / "hc_wiki_slash_commands.json"
    output_file = (
        root
        / "CityOfBinds"
        / "src"
        / "configs"
        / "valid_input"
        / "valid_slash_commands.py"
    )
    return input_file, output_file


def normalize_slash_command(slash_command: str) -> str:
    """Normalize slash command using same logic as runtime validation."""
    slash_command = slash_command.strip()
    slash_command = slash_command.replace("_", "")
    slash_command = slash_command.lower()
    return slash_command


def extract_slash_commands(data: dict) -> dict[str, str]:
    """Extract slash commands and their shortcuts from JSON data."""
    slash_commands = {}
    for item in data.get("slash_commands", []):
        slash_command = normalize_slash_command(item.get("command", ""))
        shortcut = normalize_slash_command(item.get("shortcut", ""))
        slash_commands[slash_command] = shortcut
    slash_commands[""] = ""  # Add empty command
    return slash_commands


def generate_python_code(slash_commands: dict[str, str], timestamp: str) -> str:
    """Generate the complete Python code for valid_commands.py."""
    slash_command_entires = []
    for cmd, shortcut in sorted(slash_commands.items()):
        slash_command_entires.append(f'    "{cmd}": "{shortcut}",')

    slash_commands_dict = "\n".join(slash_command_entires)

    python_code = f"""{COMMENT_BANNER.format(timestamp=timestamp)}\n\nVALID_COMMANDS: dict[str, str] = {{\n{slash_commands_dict}\n}}\n"""
    return python_code


def main():
    input_file, output_file = get_files()

    with open(input_file) as f:
        data = json.load(f)

    slash_commands = extract_slash_commands(data)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    python_code = generate_python_code(slash_commands, timestamp)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(python_code)

    print(f"Generated {len(slash_commands)} slash_commands -> {output_file}")


if __name__ == "__main__":
    main()
