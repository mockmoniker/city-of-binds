import os
from pathlib import Path
from CityOfBinds import RotatingBind, BindTemplate


class TestFileCreation:
    def test_simple_rotating_bind_file_creation(self, in_tmp_dir):
        # assemble
        powers = ["dark nova blast", "dark Nova bolt", "dark nova emmanation"]
        attack_bind_template = (
            BindTemplate("Q")
            .add_toggle_off_power("super speed")
            .add_toggle_off_power("sprint")
            .add_toggle_on_power("dark nova")
            .add_power_pool(powers)
            .add_toggle_off_power("dark nova")
        )
        rotating_bind = RotatingBind().add_bind_template(attack_bind_template)
        # act
        rotating_bind.publish_bind_files(parent_folder_name="my_rotate_bind")

        expected_files = [
            "my_rotate_bind/0.txt",
            "my_rotate_bind/1.txt",
            "my_rotate_bind/2.txt",
        ]

        for file_path in expected_files:
            assert Path(file_path).exists()

        with open(expected_files[0], "r") as f:
            contents = f.read()
        assert (
            contents
            == 'Q "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova blast$$powexectoggleoff dark nova$$bindloadfilesilent my_rotate_bind/1.txt"'
        )

        with open(expected_files[1], "r") as f:
            contents = f.read()
        assert (
            contents
            == 'Q "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova bolt$$powexectoggleoff dark nova$$bindloadfilesilent my_rotate_bind/2.txt"'
        )

        with open(expected_files[2], "r") as f:
            contents = f.read()
        assert (
            contents
            == 'Q "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova emmanation$$powexectoggleoff dark nova$$bindloadfilesilent my_rotate_bind/0.txt"'
        )

        # assert str(bind_template.build()[0]) == '1 "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova blast$$powexectoggleoff dark nova"'
        # assert str(bind_template.build()[0]) == '1 "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova bolt$$powexectoggleoff dark nova"'
        # assert str(bind_template.build()[0]) == '1 "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova emmanation$$powexectoggleoff dark nova"'
