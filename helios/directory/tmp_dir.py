import os
import shutil
from pathlib import Path
from datetime import datetime


class TempDirectory:
    def __init__(self, clean_up: bool = True):
        self._path = TempDirectory.new_path()
        self._clean_up_after_exit = clean_up
        Path(self.path).mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        # print(f'enter directory: {self.path}')
        return self

    def __exit__(self, exception, value, traceback):
        if self._clean_up_after_exit:
            self.clean_up()
            # print(f'temp directory {self.path} removed.')

    @property
    def path(self):
        return self._path

    def clean_up(self):
        if os.path.exists(self.path) and os.path.isdir(self.path):
            shutil.rmtree(self.path)

    @staticmethod
    def new_path():
        return os.path.join(
            Path.home(), 'tmp', datetime.now().strftime("%Y-%m-%d_%H%M%S")
        )
