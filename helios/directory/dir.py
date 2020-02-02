import os
from pathlib import Path


class Directory:
    def __init__(self, path: str):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)

    @property
    def full_path(self) -> str:
        return str(self._path.absolute())

    def file_list(self):
        files = []
        for f in self._path.iterdir():
            if f.is_file():
                files.append(str(f))
            else:
                if f.is_dir():
                    files = files + Directory(str(f)).file_list()
        return files

    def directory_list(self):
        dirs = []
        for d in self._path.iterdir():
            if d.is_dir():
                dirs.append(str(d))
                dirs = dirs + Directory(str(d)).directory_list()
        return dirs
