from pathlib import Path

from CityOfBinds import RandomWalk


def test_random_costumes(in_tmp_dir):

    rw = RandomWalk(exclude_jump=True, exclude_down=True)
    rw.move_bind_template.add_command_arguments_pool("cc", list(range(5)))

    # Debug: Check the unique count
    print(
        f"DEBUG: wasd_bind_template unique_count = {rw.move_bind_template.unique_count}"
    )
    print(f"DEBUG: wasd_bind_template pools = {len(rw.move_bind_template.pools)}")

    rw.publish_bind_files(
        parent_folder_name="random_costumes", directory="binds_folder"
    )

    # region validation
    # expected binds in each file
    expected_file_contents = {
        "binds_folder/random_costumes/0.txt": [
            ["W", "+forward", "bindloadfilesilent random_costumes/1.txt"],
            ["A", "+left", "bindloadfilesilent random_costumes/2.txt"],
            ["S", "+backward", "bindloadfilesilent random_costumes/3.txt"],
            ["D", "+right", "bindloadfilesilent random_costumes/4.txt"],
        ],
        "binds_folder/random_costumes/1.txt": [
            ["W", "+forward", "bindloadfilesilent random_costumes/2.txt"],
            ["A", "+left", "bindloadfilesilent random_costumes/3.txt"],
            ["S", "+backward", "bindloadfilesilent random_costumes/4.txt"],
            ["D", "+right", "bindloadfilesilent random_costumes/0.txt"],
        ],
        "binds_folder/random_costumes/2.txt": [
            ["W", "+forward", "bindloadfilesilent random_costumes/3.txt"],
            ["A", "+left", "bindloadfilesilent random_costumes/4.txt"],
            ["S", "+backward", "bindloadfilesilent random_costumes/0.txt"],
            ["D", "+right", "bindloadfilesilent random_costumes/1.txt"],
        ],
        "binds_folder/random_costumes/3.txt": [
            ["W", "+forward", "bindloadfilesilent random_costumes/4.txt"],
            ["A", "+left", "bindloadfilesilent random_costumes/0.txt"],
            ["S", "+backward", "bindloadfilesilent random_costumes/1.txt"],
            ["D", "+right", "bindloadfilesilent random_costumes/2.txt"],
        ],
        "binds_folder/random_costumes/4.txt": [
            ["W", "+forward", "bindloadfilesilent random_costumes/0.txt"],
            ["A", "+left", "bindloadfilesilent random_costumes/1.txt"],
            ["S", "+backward", "bindloadfilesilent random_costumes/2.txt"],
            ["D", "+right", "bindloadfilesilent random_costumes/3.txt"],
        ],
    }

    # verify contents of each file to ensure binds are correct
    for file_path in expected_file_contents.keys():
        assert Path(file_path).is_file()
        with open(file_path, "r") as f:
            contents = f.read()
        # print(f"DEBUG: Contents of {file_path}:")
        # print(contents)
        # print("---")
        for expected_bind_parts in expected_file_contents[file_path]:
            key, movement_command, file_load_command = expected_bind_parts
            # Check that there's a line containing all three components
            found_line_with_all_parts = False
            for line in contents.splitlines():
                if (
                    key in line
                    and movement_command in line
                    and file_load_command in line
                ):
                    found_line_with_all_parts = True
                    break
            assert (
                found_line_with_all_parts
            ), f"Could not find line with all parts: {expected_bind_parts}"
