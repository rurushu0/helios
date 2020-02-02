import chardet
from pathlib import Path
from helios.text import Encoding


class File:
    def __init__(self, file_path):
        super().__init__()
        self._path = Path(file_path)
        if not self._path.parent.exists():
            self._path.parent.mkdir()
            self._path.touch()
        self._encoding = None

    @property
    def full_path(self) -> str:
        return str(self._path.resolve())

    @property
    def size(self) -> int:
        return self._path.stat().st_size

    @property
    def encoding(self) -> Encoding:
        if not self._encoding:
            rawdata = self._path.read_bytes()
            encoding = chardet.detect(rawdata)['encoding']
            for e in Encoding:
                if encoding == e.value:
                    self._encoding = e
        return self._encoding

    def cp(self, file_output: str):
        output = File(file_output)
        output._path.write_bytes(self._path.read_bytes())
        return output

    def convert(
            self,
            file_output: str,
            encoding: Encoding = Encoding.UTF8):
        output = File(file_output)
        if self.encoding == Encoding.UTF8:
            output._path.write_bytes(self._path.read_bytes())
        else:
            context = self._path.read_text(self.encoding.value)
            output._path.write_text(context, Encoding.UTF8.value)