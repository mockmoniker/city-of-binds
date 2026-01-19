from pathlib import Path

from CityOfBinds import ChangelingWarshade


def test_small_changeling_bind_creation(in_tmp_dir):
    changeling = ChangelingWarshade(
        "SHIFT+5", power_rotation=["bolt", "blast", "detonation"]
    )

    changeling.publish_bind_files(parent_folder_name="ch", directory="binds_folder")

    # region validation
    # expected binds in each file
    expected_file_contents = {
        "binds_folder/ch/0.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova bolt$$bindloadfilesilent ch/3.txt"',
        ],
        "binds_folder/ch/3.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova bolt$$bindloadfilesilent ch/1.txt"',
        ],
        "binds_folder/ch/1.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova blast$$bindloadfilesilent ch/4.txt"',
        ],
        "binds_folder/ch/4.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova blast$$bindloadfilesilent ch/2.txt"',
        ],
        "binds_folder/ch/2.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova detonation$$bindloadfilesilent ch/5.txt"',
        ],
        "binds_folder/ch/5.txt": [
            'SHIFT+5 "+$$powexectoggleoff dark nova$$powexectoggleon dark nova$$powexecname dark nova detonation$$bindloadfilesilent ch/0.txt"',
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
