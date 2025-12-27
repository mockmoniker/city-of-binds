from pathlib import Path

from CityOfBinds import ChangelingRotatingBindWS


def test_small_changeling_bind_creation(in_tmp_dir):
    changeling = ChangelingRotatingBindWS("SHIFT+5")

    changeling.add_bolt()
    changeling.add_blast()
    changeling.add_detonation()

    changeling.publish_bind_files(parent_folder_name="ch", directory="binds_folder")

    # region validation
    # expected binds in each file
    expected_file_contents = {
        "binds_folder/ch/0.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova bolt$$powexectoggleoff dark nova$$bindloadfilesilent ch/3.txt"',
        ],
        "binds_folder/ch/3.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova bolt$$powexectoggleoff dark nova$$bindloadfilesilent ch/1.txt"',
        ],
        "binds_folder/ch/1.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova blast$$powexectoggleoff dark nova$$bindloadfilesilent ch/4.txt"',
        ],
        "binds_folder/ch/4.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova blast$$powexectoggleoff dark nova$$bindloadfilesilent ch/2.txt"',
        ],
        "binds_folder/ch/2.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova detonation$$powexectoggleoff dark nova$$bindloadfilesilent ch/5.txt"',
        ],
        "binds_folder/ch/5.txt": [
            'SHIFT+5 "+$$powexectoggleon dark nova$$powexecname dark nova detonation$$powexectoggleoff dark nova$$bindloadfilesilent ch/0.txt"',
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


def test_warshade_changeling_bind(in_tmp_dir):

    # region setup
    # initialize the rotating bind
    changeling = ChangelingRotatingBindWS("SHIFT+5")

    # define attack order
    (
        changeling.add_bolt()
        .add_blast()
        .add_bolt()
        .add_detonation()
        .add_bolt()
        .add_emmanation()
    )

    # publish the bind file
    changeling.publish_bind_files(parent_folder_name="ch")
