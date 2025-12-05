import os
import pytest


@pytest.fixture
def in_tmp_dir(tmp_path):
    """Fixture that changes working directory to tmp_path for the test duration."""
    og_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        yield tmp_path
    finally:
        os.chdir(og_cwd)
