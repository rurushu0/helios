from .dir import Directory
from ..file import File
import re


_PE = re.compile(r"[\x00-\x7f]*\.git$")


class GitDirectory(Directory):

    def is_excluded_dir(self, sub_dir: str) -> bool:
        if _PE.match(sub_dir):
            return True
        else:
            return False

    def is_excluded_file(self, file_path: str) -> bool:
        if File(file_path).is_text:
            return False
        else:
            return True
