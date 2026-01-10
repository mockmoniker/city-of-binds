from pathlib import Path

from CityOfBinds import PersistentAutos


def test_set_multiple_powers_on_auto_via_persistent_autos(in_tmp_dir):
    """
    EXAMPLE: Auto-casting Multiple Powers with Persistent Autos

    This example demonstrates how to use PersistentAutos to automatically cast
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
    4. Load the first file (0.txt) in-game with: /bindloadfile persistent_autos/0.txt

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
    # initialize the PersistentAutos with jump included
    persistent_autos = PersistentAutos(
        ["hasten", "domination", "inner inspiration"], exclude_down=True
    )

    # build and publish the bind files
    persistent_autos.publish_bind_files(
        parent_folder_name="persistent_autos", directory="binds_folder"
    )

    # endregion

    # region validation
    # expected binds in each file
    expected_file_contents = {
        "binds_folder/persistent_autos/0.txt": [
            'W "+forward$$powexecauto hasten$$bindloadfilesilent persistent_autos/1.txt"',
            'A "+left$$powexecauto hasten$$bindloadfilesilent persistent_autos/1.txt"',
            'S "+backward$$powexecauto hasten$$bindloadfilesilent persistent_autos/1.txt"',
            'D "+right$$powexecauto hasten$$bindloadfilesilent persistent_autos/1.txt"',
            'SPACE "+up$$powexecauto hasten$$bindloadfilesilent persistent_autos/1.txt"',
        ],
        "binds_folder/persistent_autos/1.txt": [
            'W "+forward$$powexecauto domination$$bindloadfilesilent persistent_autos/2.txt"',
            'A "+left$$powexecauto domination$$bindloadfilesilent persistent_autos/2.txt"',
            'S "+backward$$powexecauto domination$$bindloadfilesilent persistent_autos/2.txt"',
            'D "+right$$powexecauto domination$$bindloadfilesilent persistent_autos/2.txt"',
            'SPACE "+up$$powexecauto domination$$bindloadfilesilent persistent_autos/2.txt"',
        ],
        "binds_folder/persistent_autos/2.txt": [
            'W "+forward$$powexecauto inner inspiration$$bindloadfilesilent persistent_autos/0.txt"',
            'A "+left$$powexecauto inner inspiration$$bindloadfilesilent persistent_autos/0.txt"',
            'S "+backward$$powexecauto inner inspiration$$bindloadfilesilent persistent_autos/0.txt"',
            'D "+right$$powexecauto inner inspiration$$bindloadfilesilent persistent_autos/0.txt"',
            'SPACE "+up$$powexecauto inner inspiration$$bindloadfilesilent persistent_autos/0.txt"',
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
