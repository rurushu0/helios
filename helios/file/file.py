from pathlib import Path
from helios.text import Encoding
import chardet
import difflib
import re
from binaryornot.check import is_binary

_PATTERN_DIFF_LINE_INFO = re.compile(r"^@@[\x00-\x7f]*@@$")
_PATTERN_DIFF_LINE_LEFT = re.compile(r"^-[\x00-\x7f]*")
_PATTERN_DIFF_LINE_RIGHT = re.compile(r"^\+[\x00-\x7f]*")


class File:
    def __init__(self, file_path):
        super().__init__()
        self._path = Path(file_path)
        if not self._path.parent.exists():
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.touch()
        self._encoding = None
        self._is_text = None

    @property
    def full_path(self) -> str:
        return str(self._path.resolve())

    @property
    def size(self) -> int:
        return self._path.stat().st_size

    @property
    def is_text(self) -> bool:
        if not self._is_text:
            self._is_text = False if is_binary(self.full_path) else True
        return self._is_text

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

    @property
    def text(self) -> str:
        if self.size == 0:
            return ''
        if self.encoding:
            return self._path.read_text(self.encoding.value)
        else:
            return self._path.read_text(Encoding.UTF8.value)
            # raise Exception('File.text Error', f'{self.full_path}')
            # return self._path.read_bytes()

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

    def diff(self, rhs) -> list:
        text_lhs = self.text.splitlines()
        text_rhs = rhs.text.splitlines()
        diff_text = []
        for line in difflib.unified_diff(
            text_lhs,
            text_rhs,
            fromfile=self.full_path,
            tofile=rhs.full_path
        ):
            diff_text.append(line)
        return diff_text

    def diff_dict(self, rhs):
        result_left = dict()
        result_right = dict()
        diff_lines = self.diff(rhs)
        key = ''
        text_left = None
        text_right = None
        for line in diff_lines:
            if _PATTERN_DIFF_LINE_INFO.match(line):
                if line != key:
                    if key != '' and text_left:
                        text_left = '\n'.join(text_left)
                        result_left[key] = text_left
                        text_right = '\n'.join(text_right)
                        result_right[key] = text_right
                    key = line.replace('\n', '')
                    text_left = list()
                    text_right = list()
                    result_left[key] = text_left
                    result_right[key] = text_right
            else:
                if key != '' and _PATTERN_DIFF_LINE_LEFT.match(line):
                    text_left.append(line)
                if key != '' and _PATTERN_DIFF_LINE_RIGHT.match(line):
                    text_right.append(line)
        return (result_left, result_right)

    @staticmethod
    def rm(file):
        file._path.unlink()
