import urllib.request
from helios.directory import Directory as Dir
import os
from pathlib import Path
import subprocess

_URL_GOOGLE_JAR = 'https://github.com/google/google-java-format/releases/download/google-java-format-1.7/google-java-format-1.7-all-deps.jar'
_DEFAULT_OUTPUT_PATH = os.path.join(Path.home(), '.java_lib')
_DEFAULT_JAR_NAME = 'google-java-formatter.jar'


def _defaut_formatter_path() -> str:
    return os.path.join(
        _DEFAULT_OUTPUT_PATH,
        _DEFAULT_JAR_NAME
    )


def _download_google_formater(download_path: str = _DEFAULT_OUTPUT_PATH):
    dir_output = Dir(download_path)
    file_path = os.path.join(dir_output.full_path, _DEFAULT_JAR_NAME)
    urllib.request.urlretrieve(
        _URL_GOOGLE_JAR,
        file_path)


class JavaSourceFormatter:
    _CMD = ['java', '-jar', _DEFAULT_JAR_NAME, '--replace']

    def __init__(self):
        self._formatter_path = _defaut_formatter_path()

        if not Path(self.formater_path).exists():
            _download_google_formater()

    @property
    def formater_path(self) -> str:
        return self._formatter_path

    @staticmethod
    def execute(files: list, is_verbose=False):
        for file in files:
            cmd = ' '.join(JavaSourceFormatter._CMD + [file])
            if is_verbose:
                print(f'format java file: {file}')
            subprocess.run(args=cmd, cwd=_DEFAULT_OUTPUT_PATH, shell=True)
