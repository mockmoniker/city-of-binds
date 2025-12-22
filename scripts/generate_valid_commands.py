#!/usr/bin/env python3
"""
Simple generator to create valid_commands.py from template and JSON data
"""

import json
from pathlib import Path
from datetime import datetime, timezone


def normalize_slash_command(slash_command: str) -> str:
    slash_command = slash_command.strip()
    slash_command = slash_command.replace("_", "")
    slash_command = slash_command.lower()
    return slash_command


def main():
    # File paths
    project_root = Path(__file__).parent.parent
    json_file = project_root / "resources" / "hc_wiki_slash_commands.json"
    template_file = (
        project_root / "scripts" / "templates" / "valid_commands.template.py"
    )
    output_file = (
        project_root
        / "CityOfBinds"
        / "src"
        / "game"
        / "utils"
        / "commands"
        / "valid_commands.py"
    )

    # Load JSON data
    with open(json_file) as f:
        data = json.load(f)

    # Load template
    with open(template_file) as f:
        template = f.read()

    # Extract commands
    commands = {}
    for item in data.get("slash_commands", []):
        command = normalize_slash_command(item.get("command", ""))
        shortcut = normalize_slash_command(item.get("shortcut", ""))
        if command:
            commands[command] = shortcut

    commands[""] = ""  # Add empty command

    # Generate commands dictionary entries with proper formatting
    commands_entries = "\n".join(
        f'    "{cmd}": "{shortcut}",' for cmd, shortcut in sorted(commands.items())
    )
    commands_dict = f"{{\n{commands_entries}\n}}"

    # Fill template placeholders
    python_code = template.format(
        DATE=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        DO_NOT_EDIT_NOTICE="DO NOT EDIT - Run scripts/generate_valid_commands.py to regenerate",
        COMMANDS=commands_dict,
    )
    python_code = python_code.replace("  # type: ignore", "")

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(python_code)

    print(f"Generated {len(commands)} commands -> {output_file}")


if __name__ == "__main__":
    main()
