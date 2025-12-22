#!/usr/bin/env python3
"""
Generate valid_commands.py directly from JSON data
"""

import json
from pathlib import Path
from datetime import datetime, timezone


def normalize_slash_command(slash_command: str) -> str:
    """Normalize slash command using same logic as runtime validation."""
    slash_command = slash_command.strip()
    slash_command = slash_command.replace("_", "")
    slash_command = slash_command.lower()
    return slash_command


def main():
    # File paths
    root = Path(__file__).parent.parent
    json_file = root / "resources" / "hc_wiki_slash_commands.json"
    output_file = (
        root / "CityOfBinds" / "src" / "configs" / "valid_input" / "valid_commands.py"
    )

    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)

    # Extract commands
    commands = {}
    for item in data.get("slash_commands", []):
        command = item.get("command", "").strip()
        shortcut = item.get("shortcut", "").strip()
        if command:
            normalized_cmd = normalize_slash_command(command)
            normalized_shortcut = (
                normalize_slash_command(shortcut) if shortcut else normalized_cmd
            )
            commands[normalized_cmd] = normalized_shortcut

    commands[""] = ""  # Add empty command

    # Generate the complete Python file
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Build commands dictionary entries
    command_entries = []
    for cmd, shortcut in sorted(commands.items()):
        command_entries.append(f'    "{cmd}": "{shortcut}",')

    commands_dict = "\n".join(command_entries)

    # Build the complete file content
    python_code = f'''"""
Generated: {timestamp}

DO NOT EDIT - Run scripts/generate_valid_commands.py to regenerate
"""

VALID_COMMANDS: dict[str, str] = {{
{commands_dict}
}}
'''

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(python_code)

    print(f"Generated {len(commands)} commands -> {output_file}")


if __name__ == "__main__":
    main()
