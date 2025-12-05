import pytest
from CityOfBinds import BindFile, Bind
from CityOfBinds.src.game.utils import _CommentBanner


class TestBindFilePreview:
    bindfile_under_test = BindFile

    def test_preview_should_return_empty_string_given_empty_bindfile(self):
        # arrange
        bindfile = self.bindfile_under_test()
        # act
        preview = bindfile.preview()
        # assert
        assert preview == ""

    def test_preview_should_return_correct_string_given_bindfile_with_multiple_binds(
        self,
    ):
        # arrange
        bindfile = (
            BindFile()
            .add_bind(Bind("F", ["powexectoggleon dark nova"]))
            .add_bind(
                Bind("G", ["powexectoggleon light nova", "powexectoggleon speed boost"])
            )
        )
        # act
        preview = bindfile.preview()
        # assert
        assert preview == (
            'F "powexectoggleon dark nova"\n'
            'G "powexectoggleon light nova$$powexectoggleon speed boost"'
        )


class TestBindFileWriteToFile:
    bindfile_under_test = BindFile

    def test_write_to_file_should_create_file_with_correct_contents(self, tmp_path):
        # arrange
        bindfile = (
            BindFile()
            .add_bind(Bind("F", ["powexectoggleon dark nova"]))
            .add_bind(
                Bind("G", ["powexectoggleon light nova", "powexectoggleon speed boost"])
            )
        )
        file_path = tmp_path / "test_bindfile.txt"
        # act
        bindfile.write_to_file(file_path)
        # assert
        with open(file_path, "r") as f:
            actual_contents = f.read()
        assert actual_contents == (
            'F "powexectoggleon dark nova"\n'
            'G "powexectoggleon light nova$$powexectoggleon speed boost"'
        )

    def test_write_to_file_should_create_file_given_binds_and_comments(self, tmp_path):
        # arrange
        bindfile = (
            BindFile()
            .add_comment(_CommentBanner("Start of Binds", border_style="-"))
            .add_bind(Bind("F", ["powexectoggleon dark nova"]))
            .add_comment(_CommentBanner("End of Binds", border_style="="))
            .add_bind(
                Bind("G", ["powexectoggleon light nova", "powexectoggleon speed boost"])
            )
        )
        file_path = tmp_path / "test_bindfile_with_comments.txt"
        # act
        bindfile.write_to_file(file_path)
        # assert
        with open(file_path, "r") as f:
            actual_contents = f.read()
        expected_contents = (
            "# -------------- #\n"
            "# Start of Binds #\n"
            "# -------------- #\n"
            'F "powexectoggleon dark nova"\n'
            "# ============ #\n"
            "# End of Binds #\n"
            "# ============ #\n"
            'G "powexectoggleon light nova$$powexectoggleon speed boost"'
        )
        assert actual_contents == expected_contents

    def tesT_write_to_file_should_auto_add_txt_extension_if_missing(self, tmp_path):
        # arrange
        bindfile = BindFile().add_bind(Bind("F", ["powexectoggleon dark nova"]))
        file_path = tmp_path / "test_bindfile"  # No .txt extension
        # act
        bindfile.write_to_file(file_path)
        # assert
        expected_file_path = tmp_path / "test_bindfile.txt"
        assert expected_file_path.exists()
        with open(expected_file_path, "r") as f:
            actual_contents = f.read()
        assert actual_contents == 'F "powexectoggleon dark nova"'
