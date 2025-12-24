from pathlib import Path
from CityOfBinds import WASDRotatingBind


def test_set_multiple_powers_on_auto_via_wasd_rotating_bind(in_tmp_dir):
    """Should create multiple bind files that will cycle through auto powers when pressing WASD keys."""

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

    # expected files to be created
    expected_files = [
        "binds_folder/auto_powers/0.txt",
        "binds_folder/auto_powers/1.txt",
        "binds_folder/auto_powers/2.txt",
    ]

    # verify that all expected files were created
    for file_path in expected_files:
        assert Path(file_path).is_file()

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
        with open(file_path, "r") as f:
            contents = f.read()
        for expected_bind in expected_file_contents[file_path]:
            assert expected_bind in contents

    # endregion
