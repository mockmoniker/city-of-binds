from pathlib import Path

from CityOfBinds import WASDRotatingBind


def test_set_multiple_powers_on_auto_via_wasd_rotating_bind(in_tmp_dir):
    """
    EXAMPLE: Auto-casting Multiple Powers with WASD Rotating Binds

    This example demonstrates how to use WASDRotatingBind to automatically cast
    multiple powers while moving with WASD keys. This is particularly useful for
    Dominators who want to keep both Hasten and Domination on auto-cast, plus
    Inner Inspiration for free inspirations.

    HOW IT WORKS:
    - Creates 3 bind files that rotate through each power when you press WASD keys
    - Each movement key (W/A/S/D/SPACE) will cast one power and load the next file
    - This ensures all powers stay on auto-cast without manual clicking
    - Powers cycle: Hasten → Domination → Inner Inspiration → (repeat)

    TO USE THIS EXAMPLE:
    1. The WASDRotatingBind comes with a built-in wasd_bind_template
    2. Add your desired auto powers to this template using add_auto_power_pool()
    3. Call publish_bind_files() to generate the rotating bind files
    4. Load the first file (0.txt) in-game with: /bindloadfile auto_powers/0.txt

    CUSTOMIZATION:
    - Change the power list ["hasten", "domination", "inner inspiration"] to your needs
    - Set include_jump=True to include SPACE key for 5-key movement
    - parent_folder_name: Creates a new folder to hold all your bind files
    - directory: Where the parent folder will be created (ideally your City of Heroes
      default folder - see https://homecoming.wiki/wiki/Default_Folder for location)

    RESULT:
    - Moving with WASD automatically casts powers in rotation
    - Never have to worry about manually refreshing auto powers
    - Perfect for keeping buffs active during combat
    """

    # region setup

    # initialize the WASDRotatingBind with jump included
    wasd_rotating_bind = WASDRotatingBind(include_jump=True)

    # add auto power pool to the built in wasd_bind_template
    wasd_rotating_bind.wasd_bind_template.add_auto_power_pool(
        ["hasten", "domination", "inner inspiration"]
    )

    # build and publish the bind files
    wasd_rotating_bind.publish_bind_files(
        parent_folder_name="auto_powers", directory="binds_folder"
    )

    # endregion

    # region validation

    # expected binds in each file
    expected_file_contents = {
        "binds_folder/auto_powers/0.txt": [
            'W "+forward$$powexecauto hasten$$bindloadfilesilent auto_powers/1.txt"',
            'A "+left$$powexecauto hasten$$bindloadfilesilent auto_powers/1.txt"',
            'S "+backward$$powexecauto hasten$$bindloadfilesilent auto_powers/1.txt"',
            'D "+right$$powexecauto hasten$$bindloadfilesilent auto_powers/1.txt"',
            'SPACE "+up$$powexecauto hasten$$bindloadfilesilent auto_powers/1.txt"',
        ],
        "binds_folder/auto_powers/1.txt": [
            'W "+forward$$powexecauto domination$$bindloadfilesilent auto_powers/2.txt"',
            'A "+left$$powexecauto domination$$bindloadfilesilent auto_powers/2.txt"',
            'S "+backward$$powexecauto domination$$bindloadfilesilent auto_powers/2.txt"',
            'D "+right$$powexecauto domination$$bindloadfilesilent auto_powers/2.txt"',
            'SPACE "+up$$powexecauto domination$$bindloadfilesilent auto_powers/2.txt"',
        ],
        "binds_folder/auto_powers/2.txt": [
            'W "+forward$$powexecauto inner inspiration$$bindloadfilesilent auto_powers/0.txt"',
            'A "+left$$powexecauto inner inspiration$$bindloadfilesilent auto_powers/0.txt"',
            'S "+backward$$powexecauto inner inspiration$$bindloadfilesilent auto_powers/0.txt"',
            'D "+right$$powexecauto inner inspiration$$bindloadfilesilent auto_powers/0.txt"',
            'SPACE "+up$$powexecauto inner inspiration$$bindloadfilesilent auto_powers/0.txt"',
        ],
    }

    # verify contents of each file to ensure binds are correct
    for file_path in expected_file_contents.keys():
        assert Path(file_path).is_file()
        with open(file_path, "r") as f:
            contents = f.read()
        for expected_bind in expected_file_contents[file_path]:
            assert expected_bind in contents

    # endregion
