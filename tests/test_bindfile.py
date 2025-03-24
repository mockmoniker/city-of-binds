import pytest
from CityOfBinds import BindFile, Bind

class TestValidBindFileInitialization:
    bindfile_under_test = BindFile

    def test_init_should_set_filename_given_valid_filename(self):
        # arrange
        valid_filename = 'bindfile.txt'
        # act
        bindfile = self.bindfile_under_test(filename=valid_filename)
        # assert
        assert bindfile.filename == valid_filename

    def test_init_should_set_comment_banner_given_valid_comment_banner(self):
        # arrange
        valid_comment_banner = 'This is a comment'
        # act
        bindfile = self.bindfile_under_test(filename='bindfile.txt', comment_banner=valid_comment_banner)
        # assert
        assert bindfile.comment_banner == valid_comment_banner

    def test_init_should_set_binds_given_valid_binds(self):
        # arrange
        valid_binds = [Bind(trigger='Q', slash_commands=['powexectoggleon dark nova']), Bind(trigger='E', slash_commands=['powexectoggleon black dwarf'])]
        # act
        bindfile = self.bindfile_under_test(filename='bindfile.txt', binds=valid_binds)
        # assert
        assert bindfile.binds == valid_binds

class TestValidFileCreation:
    bindfile_under_test = BindFile

    def test_write_to_file_should_create_file(self, tmp_path):
        # arrange
        bindfile = self.bindfile_under_test(filename='bindfile.txt')
        epxected_file = tmp_path / 'bindfile.txt'
        # act
        bindfile.write_to_file(path=tmp_path)
        # assert
        assert epxected_file.exists()

    def test_write_to_file_should_write_bind_to_file(self, tmp_path):
        # arrange
        bindfile = self.bindfile_under_test(filename='bindfile.txt', comment_banner='This is a comment', binds=[Bind(trigger='Q', slash_commands=['powexectoggleon dark nova'])])
        expected_content = (
            '#\n'
            '# This is a comment\n'
            '#\n'
            'Q "powexectoggleon dark nova"\n')
        # act
        bindfile.write_to_file(path=tmp_path)
        # assert
        with open(tmp_path / 'bindfile.txt', 'r') as file:
            content = file.read()
            assert content == expected_content

    def test_write_to_file_should_write_multiple_binds_to_file(self, tmp_path):
        # arrange
        bindfile = self.bindfile_under_test(filename='bindfile.txt', comment_banner='This is a comment', binds=[Bind(trigger='Q', slash_commands=['powexectoggleon dark nova']), Bind(trigger='E', slash_commands=['powexectoggleon black dwarf'])])
        expected_content = (
            '#\n'
            '# This is a comment\n'
            '#\n'
            'Q "powexectoggleon dark nova"\n'
            'E "powexectoggleon black dwarf"\n')
        # act
        bindfile.write_to_file(path=tmp_path)
        # assert
        with open(tmp_path / 'bindfile.txt', 'r') as file:
            content = file.read()
            assert content == expected_content
    