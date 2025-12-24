from pathlib import Path
from CityOfBinds import WASDRotatingBind


def test_keep_powers_perstent_via_wasd_rotating_bind(in_tmp_dir):
    """
    EXAMPLE: Automated Toggle Management with WASD Rotating Binds

    This example demonstrates how to automatically manage multiple types of powers
    (toggles, auto powers) using just your WASD movement keys. Perfect for characters
    like Warshades who need to juggle many different toggle states while playing.

    HOW IT WORKS:
    - Creates 4 bind files that rotate through different power combinations
    - Each time you press WASD keys, powers get turned on/off and files rotate
    - Toggle-OFF powers (transformations) stay disabled to keep human form
    - Toggle-ON powers (travel powers) get turned on regularly in case they drop
    - Power pools rotate through different options, giving each regular chances to activate
    - Auto powers alternate between different buffs as you move around

    TO USE THIS EXAMPLE:
    1. The WASDRotatingBind comes with a built-in wasd_bind_template
    2. Add toggle-off powers for things you want to stay disabled
    3. Add individual toggle-on powers for critical abilities (travel powers)
    4. Add toggle-on power pools for defensive abilities you want rotating opportunities
    5. Add auto power pools for buffs you want alternating as you move
    6. Call publish_bind_files() to generate the rotating bind files
    7. Load the first file in-game: /bindloadfile wasd/0.txt

    CUSTOMIZATION:
    - Toggle-off powers: Replace ["dark nova", "black dwarf"] with unwanted toggles
    - High-priority toggles: Add individual powers with add_toggle_on_power()
    - Rotating toggles: Use add_toggle_on_power_pool() for defensive abilities
    - Auto powers: Use add_auto_power_pool() for buffs you want cycling
    - parent_folder_name: Creates a new folder to hold all your bind files
    - directory: Where the parent folder will be created (ideally your City of Heroes
      default folder - see https://homecoming.wiki/wiki/Default_Folder for location)

    This creates hands-free power management - just play normally and your character
    automatically maintains the right power states through regular movement.
    """

    # region setup

    # initialize the WASDRotatingBind with jump included
    wasd_rotating_bind = WASDRotatingBind()

    # add various persistent toggle and auto power pools to the built in wasd_bind_template
    (
        wasd_rotating_bind.wasd_bind_template.add_toggle_off_power("dark nova")
        .add_toggle_off_power("black dwarf")
        .add_toggle_on_power_pool(
            ["gravity shield", "penumbral shield", "twilight shield", "shadow cloak"]
        )
        .add_toggle_on_power("sprint")
        .add_toggle_on_power("super speed")
        .add_auto_power_pool(["hasten", "ageless core epiphany"])
    )

    # publish files
    wasd_rotating_bind.publish_bind_files(
        parent_folder_name="wasd", directory="binds_folder"
    )

    # endregion

    # region validation

    # expected binds in each file
    expected_file_contents = {
        "binds_folder/wasd/0.txt": [
            'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon gravity shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/1.txt"',
            'A "+left$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon gravity shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/1.txt"',
            'S "+backward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon gravity shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/1.txt"',
            'D "+right$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon gravity shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/1.txt"',
        ],
        "binds_folder/wasd/1.txt": [
            'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon penumbral shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/2.txt"',
            'A "+left$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon penumbral shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/2.txt"',
            'S "+backward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon penumbral shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/2.txt"',
            'D "+right$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon penumbral shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/2.txt"',
        ],
        "binds_folder/wasd/2.txt": [
            'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon twilight shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/3.txt"',
            'A "+left$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon twilight shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/3.txt"',
            'S "+backward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon twilight shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/3.txt"',
            'D "+right$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon twilight shield$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto hasten$$bindloadfilesilent wasd/3.txt"',
        ],
        "binds_folder/wasd/3.txt": [
            'W "+forward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon shadow cloak$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/0.txt"',
            'A "+left$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon shadow cloak$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/0.txt"',
            'S "+backward$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon shadow cloak$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/0.txt"',
            'D "+right$$powexectoggleoff dark nova$$powexectoggleoff black dwarf$$powexectoggleon shadow cloak$$powexectoggleon sprint$$powexectoggleon super speed$$powexecauto ageless core epiphany$$bindloadfilesilent wasd/0.txt"',
        ],
    }

    # verify contents of each file to ensure binds are correct
    for file_path in expected_file_contents.keys():
        assert Path(file_path).is_file()
        with open(file_path, "r") as f:
            contents = f.read()
        for expected_bind in expected_file_contents[file_path]:
            assert expected_bind in contents
