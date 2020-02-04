from pathlib import Path
from .file_diff import FilesDiff
import os
import shutil


class Directory(object):
    def __init__(self, path: str):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)

    @property
    def full_path(self) -> str:
        return str(self._path.absolute())

    def file_list(self, is_relative_path: bool = False) -> list:
        return self._file_list_impl(self.full_path, is_relative_path)

    @staticmethod
    def remove(path: str):
        shutil.rmtree(path, ignore_errors=True)

    def _file_list_impl(
            self,
            root_path: str,
            is_relative_path: bool = False
    ) -> list:
        files = []
        for f in self._path.iterdir():
            if f.is_file():
                if not is_relative_path:
                    if not self.is_excluded_file(str(f)):
                        files.append(str(f))
                else:
                    files.append(
                        str(f).replace(root_path, '')[1:]
                    )
            else:
                if f.is_dir() and not self.is_excluded_dir(str(f)):
                    files = files + \
                        Directory(str(f))._file_list_impl(
                            root_path, is_relative_path)
        return files

    def directory_list(self) -> list:
        dirs = []
        for d in self._path.iterdir():
            if d.is_dir():
                dirs.append(str(d))
                dirs = dirs + Directory(str(d)).directory_list()
        return dirs

    def diff_files(self, rhs) -> FilesDiff:
        files_lhs = set(list(self.file_list(True)))
        files_rhs = set(list(rhs.file_list(True)))
        both = files_lhs & files_rhs
        return FilesDiff(
            both=sorted(list(both)),
            left_only=sorted(list(map(lambda x: os.path.join(
                self.full_path, x), files_lhs - both))),
            right_only=sorted(list(map(lambda x: os.path.join(
                rhs.full_path, x), files_rhs - both)))
        )

    def is_excluded_dir(self, sub_dir: str) -> bool:
        return False

    def is_excluded_file(self, file_path: str) -> bool:
        return False
