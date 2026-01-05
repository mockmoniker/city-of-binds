from pathlib import Path

from CityOfBinds import BindTemplate, RotatingBind


def test_safe_install_file_creation(in_tmp_dir):
    rb = RotatingBind()
    rb.add_bind_template(
        BindTemplate("F1").add_command_arguments_pool("say", ["Hey", "Hi", "Wuz up?"])
    )

    # build and publish the bind files
    rb.publish_bind_files(parent_folder_name="greetings", directory="binds_folder")

    # region validation
    # expected binds in each file
    expected_file_contents = {
        "binds_folder/greetings/0.txt": [
            'F1 "say Hey$$bindloadfilesilent greetings/1.txt"',
        ],
        "binds_folder/greetings/1.txt": [
            'F1 "say Hi$$bindloadfilesilent greetings/2.txt"',
        ],
        "binds_folder/greetings/2.txt": [
            'F1 "say Wuz up?$$bindloadfilesilent greetings/0.txt"',
        ],
        "binds_folder/greetings/_install.txt": [
            'KANA "nop"$$macroimage "InherentBase_Fury" "Safe Load" "bindloadfilesilent greetings/_load.txt"',
            'KANA "nop"$$macroimage "InherentBase_Anger" "Safe Unload" "bindloadfilesilent greetings/_unload.txt"',
            'KANA "nop"$$showbindallfile greetings/_install.txt$$bindloadfilesilent greetings/_load.txt',
        ],
        "binds_folder/greetings/_load.txt": [
            'KANA "nop"$$bindloadfilesilent greetings/0.txt',
        ],
        "binds_folder/greetings/_unload.txt": [
            'KANA "nop"$$bindloadfilesilent greetings/_install.txt',
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
