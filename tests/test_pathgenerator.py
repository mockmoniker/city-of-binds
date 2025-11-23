from CityOfBinds import PathGenerator

class TestPathGenerator:
    def test_default_generator_should_return_correct_files_without_folders(self):
        # arrange
        path_generator = PathGenerator(file_count = 256)  # No folders
        file_index_0 = 0
        file_index_1 = 1
        file_index_10 = 10  
        file_index_16 = 16  
        file_index_100 = 100
        file_index_254 = 254
        file_index_255 = 255
        # act
        path_0 = path_generator[file_index_0]
        path_1 = path_generator[file_index_1]
        path_10 = path_generator[file_index_10]
        path_16 = path_generator[file_index_16]
        path_100 = path_generator[file_index_100]
        path_254 = path_generator[file_index_254]
        path_255 = path_generator[file_index_255]
        # assert
        assert str(path_0) == "00.txt"
        assert str(path_1) == "01.txt"
        assert str(path_10) == "0A.txt" 
        assert str(path_16) == "10.txt"
        assert str(path_100) == "64.txt"
        assert str(path_254) == "FE.txt"
        assert str(path_255) == "FF.txt"

    def test_default_generator_should_return_correct_files_with_folders(self):
        # arrange
        path_generator = PathGenerator(file_count = 65536)  # 256 files per folder, 256 folders
        file_index_0 = 0
        file_index_1 = 1
        file_index_255 = 255
        file_index_256 = 256
        file_index_257 = 257
        file_index_65534 = 65534
        file_index_65535 = 65535
        # act
        path_0 = path_generator[file_index_0]
        path_1 = path_generator[file_index_1]
        path_255 = path_generator[file_index_255]
        path_256 = path_generator[file_index_256]
        path_257 = path_generator[file_index_257]
        path_65534 = path_generator[file_index_65534]
        path_65535 = path_generator[file_index_65535]
        # assert
        assert str(path_0) == "00/00.txt"
        assert str(path_1) == "00/01.txt"
        assert str(path_255) == "00/FF.txt"
        assert str(path_256) == "01/00.txt"
        assert str(path_257) == "01/01.txt"
        assert str(path_65534) == "FF/FE.txt"
        assert str(path_65535) == "FF/FF.txt"

    def test_default_generator_should_return_efficiently_padded_paths(self):
        # arrange
        path_generator = PathGenerator(file_count = 4096)
        file_index_0 = 0
        file_index_1 = 1
        file_index_255 = 255
        file_index_256 = 256
        file_index_257 = 257
        file_index_4094 = 4094
        file_index_4095 = 4095
        # act
        path_0 = path_generator[file_index_0]
        path_1 = path_generator[file_index_1]
        path_255 = path_generator[file_index_255]
        path_256 = path_generator[file_index_256]
        path_257 = path_generator[file_index_257]
        path_4094 = path_generator[file_index_4094]
        path_4095 = path_generator[file_index_4095]
        # assert
        assert str(path_0) == "0/00.txt"
        assert str(path_1) == "0/01.txt"
        assert str(path_255) == "0/FF.txt"
        assert str(path_256) == "1/00.txt"
        assert str(path_257) == "1/01.txt"
        assert str(path_4094) == "F/FE.txt"
        assert str(path_4095) == "F/FF.txt"