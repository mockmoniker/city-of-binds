from CityOfBinds import PathGenerator

class TestPathGenerator:
    def test_default_generator_should_return_correct_files_without_folders(self):
        # arrange
        path_generator = PathGenerator(file_count = 256)  # No folders
        # act / assert
        assert str(path_generator[0]) == "00.txt"
        assert str(path_generator[1]) == "01.txt"
        assert str(path_generator[10]) == "0A.txt" 
        assert str(path_generator[16]) == "10.txt"
        assert str(path_generator[100]) == "64.txt"
        assert str(path_generator[254]) == "FE.txt"
        assert str(path_generator[255]) == "FF.txt"

    def test_default_generator_should_return_correct_files_with_folders(self):
        # arrange
        path_generator = PathGenerator(file_count = 65536)
        # act / assert
        assert str(path_generator[0]) == "00/00.txt"
        assert str(path_generator[1]) == "00/01.txt"
        assert str(path_generator[255]) == "00/FF.txt"
        assert str(path_generator[256]) == "01/00.txt"
        assert str(path_generator[257]) == "01/01.txt"
        assert str(path_generator[65534]) == "FF/FE.txt"
        assert str(path_generator[65535]) == "FF/FF.txt"

    def test_default_generator_should_return_efficiently_padded_paths(self):
        # arrange
        path_generator = PathGenerator(file_count = 4096)
        # act / assert
        assert str(path_generator[0]) == "0/00.txt"
        assert str(path_generator[1]) == "0/01.txt"
        assert str(path_generator[255]) == "0/FF.txt"
        assert str(path_generator[256]) == "1/00.txt"
        assert str(path_generator[257]) == "1/01.txt"
        assert str(path_generator[4094]) == "F/FE.txt"
        assert str(path_generator[4095]) == "F/FF.txt"