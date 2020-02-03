from pathlib import Path


class Directory:
    def __init__(self, path: str):
        self._path = Path(path)
        if not self._path.exists():
            self._path.mkdir(parents=True, exist_ok=True)

    @property
    def full_path(self) -> str:
        return str(self._path.absolute())

    def file_list(self, is_relative_path: bool = False) -> list:
        return self._file_list_impl(self.full_path, is_relative_path)

    def _file_list_impl(
            self,
            root_path: str,
            is_relative_path: bool = False
    ) -> list:
        files = []
        for f in self._path.iterdir():
            if f.is_file():
                if not is_relative_path:
                    files.append(str(f))
                else:
                    files.append(
                        str(f).replace(root_path, '')[1:]
                    )
            else:
                if f.is_dir():
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
