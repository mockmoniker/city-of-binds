import pytest
from CityOfBinds import RotatingBind, Bind

class TestValidRotatingBindInitialization:
    rotatingbind_under_test = RotatingBind

    def test_init_should_set_bind_list_given_valid_bind_list(self):
        # arrange
        toggleNovaBind1 = Bind(trigger="Q", slash_commands=["powexectoggleon dark nova"])
        toggleNovaBind2 = Bind(trigger="Q", slash_commands=["powexectoggleoff dark nova"])
        valid_bind_list = [toggleNovaBind1, toggleNovaBind2]
        # act
        rotatingbind = self.rotatingbind_under_test(bind_list=valid_bind_list)
        # assert
        assert rotatingbind.bind_list == valid_bind_list

class TestInvalidRotatingBindInitialization:
    rotatingbind_under_test = RotatingBind

    def test_init_should_throw_error_given_invalid_bind_list(self):
        # arrange
        invalid_bind_list = []
        # act/ assert
        with pytest.raises(ValueError, match="Bind list cannot be empty"):
            self.rotatingbind_under_test(bind_list=invalid_bind_list)

class TestRotatingBindFileCreation:
    rotatingbind_under_test = RotatingBind

    def test_publish_rotating_bind_files_should_create_files(self, tmp_path):
        # arrange
        bind1 = Bind(trigger="Q", slash_commands=["powexectoggleon dark nova"])
        bind2 = Bind(trigger="Q", slash_commands=["powexectoggleoff dark nova"])
        rotatingbind = self.rotatingbind_under_test(bind_list=[bind1, bind2])
        expected_file1 = tmp_path / '0.txt'
        expected_file2 = tmp_path / '1.txt'
        # act
        rotatingbind.publish_rotating_bind_files(path=tmp_path)
        # assert
        assert expected_file1.exists()
        assert expected_file2.exists()


