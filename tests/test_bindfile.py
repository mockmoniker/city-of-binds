import pytest
from CityOfBinds import BindFile
from parameters.test_bindfile_parameters import TestBindFileParameters

class TestValidBindFileInitialization:
    bindfile_under_test = BindFile
    default_filename = "bind.txt"

    @pytest.mark.parametrize("valid_filename, expected_filename", TestBindFileParameters.test_init_should_set_filename_given_valid_filename_parameters)
    def test_init_should_set_filename_given_valid_filename(self, valid_filename, expected_filename):
        bindfile = self.bindfile_under_test(filename=valid_filename)
        assert bindfile.filename == expected_filename

    @pytest.mark.parametrize("valid_comment_banner, expected_comment_banner", TestBindFileParameters.test_init_should_set_comment_banner_given_valid_comment_banner_parameters)
    def test_init_should_set_comment_banner_given_valid_comment_banner(self, valid_comment_banner, expected_comment_banner):
        bindfile = self.bindfile_under_test(filename=self.default_filename, comment_banner=valid_comment_banner)
        assert bindfile.comment_banner == expected_comment_banner

    @pytest.mark.parametrize("valid_binds, expected_binds", TestBindFileParameters.test_init_should_set_binds_given_valid_binds_parameters)
    def test_init_should_set_binds_given_valid_binds(self, valid_binds, expected_binds):
        bindfile = self.bindfile_under_test(filename=self.default_filename, binds=valid_binds)
        assert bindfile.binds == expected_binds

class TestValidFileCreation:
    bindfile_under_test = BindFile
    default_filename = "bind.txt"
    default_comment_banner = "This is a comment"

    