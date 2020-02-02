# import unittest
from pathlib import Path
from helios.directory import TempDirectory as TmpDir


# class TestTempDir(unittest.TestCase):
def test_tmp_dir():
    with TmpDir() as tmp_dir:
        print(tmp_dir.path)
        assert Path(tmp_dir.path).exists(
        ), "helios.directory.TempDirectory init() failed."
