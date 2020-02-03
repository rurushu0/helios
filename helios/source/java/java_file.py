from helios.file import File
import javaproperties
import re

_PATTERN_JAVA = re.compile(r"([A-Za-z\-'\.^\W\d_ ]*)\.java$")


class JavaSourceFile(File):
    def __init__(self, file_path):
        super().__init__(file_path)
        with open(file_path, 'r', encoding=self.encoding.value) as fp:
            self._properties = javaproperties.load(fp)

    @property
    def properties(self) -> dict:
        return self._properties

    @staticmethod
    def is_java_file_name(file_path: str) -> bool:
        return _PATTERN_JAVA.match(file_path)
