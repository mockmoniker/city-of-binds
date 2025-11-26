from CityOfBinds import RotatingBind, Bind

class TestInitialization:
    def test_init_should_accept_binds_list(self):
        # arrange
        binds = []
        # act
        rotating_bind = RotatingBind(binds)
        # assert
        assert rotating_bind.binds == binds

    def test_init_should_accept_is_circular_flag(self):
        # arrange
        binds = []
        is_circular = False
        # act
        rotating_bind = RotatingBind(binds, is_circular)
        # assert
        assert rotating_bind.is_circular == is_circular

class TestFileCreation:
    def test_simple_rotating_bind_file_creation(self, tmp_path):
        # arrange
        binds = [
            Bind('H', ['say Hello!']),
            Bind('H', ['say Howdy!']),
            Bind('H', ['say Yo!']),
            Bind('H', ['say Hey there!']),
        ]
        rotating_bind = RotatingBind(binds)
        # act
        rotating_bind.publish(tmp_path / "hello")
        # assert
        expected_files = [
            tmp_path / "hello/0.txt",
            tmp_path / "hello/1.txt",
            tmp_path / "hello/2.txt",
            tmp_path / "hello/3.txt",
        ]
        for file_path in expected_files:
            assert file_path.exists()
        with open(expected_files[0], 'r') as f:
            contents = f.read()
        assert f'H "say Hello!$$bindloadfilesilent {str(tmp_path)}/hello/1.txt"' in contents
        with open(expected_files[3], 'r') as f:
            contents = f.read()
        assert f'H "say Hey there!$$bindloadfilesilent {str(tmp_path)}/hello/0.txt"' in contents
