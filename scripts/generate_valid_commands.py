#!/usr/bin/env python3
"""
Simple generator to create valid_commands.py from hc_wiki_slash_commands.json
"""

import json
from pathlib import Path


def main():
    # File paths
    project_root = Path(__file__).parent.parent
    json_file = project_root / "resources" / "hc_wiki_slash_commands.json"
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

    # Extract commands
    commands = {}
    for item in data.get("slash_commands", []):
        command = item.get("command", "").strip()
        shortcut = item.get("shortcut", "").strip()
        if command:
            commands[command] = shortcut

    # Generate Python code
    commands_dict = "\n".join(
        f'    "{cmd}": "{shortcut}",' for cmd, shortcut in sorted(commands.items())
    )

    python_code = (
        f'"""\n'
        f"Auto-generated slash commands for City of Heroes.\n"
        f"DO NOT EDIT - Run scripts/generate_valid_commands.py to regenerate\n"
        f'"""\n\n'
        f"from typing import Dict, Set\n\n"
        f'VALID_PREFIXES: Set[str] = {{"--", "++", "-", "+"}}\n\n'
        f"VALID_COMMANDS: Dict[str, str] = {{\n"
        f"{commands_dict}\n"
        f"}}\n"
    )

    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        f.write(python_code)

    print(f"Generated {len(commands)} commands -> {output_file}")


if __name__ == "__main__":
    main()
