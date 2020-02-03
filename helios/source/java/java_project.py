from helios.directory import Directory
from helios.source.comparsion import FilesDiff
from .java_file import JavaSourceFile
import os


class JavaProject:
    def __init__(self, path: str):
        self._project_dir = Directory(path)

    @property
    def java_source_files(self):
        for file in self._project_dir.file_list(is_relative_path=True):
            if JavaSourceFile.is_java_file_name(file):
                yield file
        # return list(filter(
        #    lambda x: JavaSourceFile.is_java_file_name(x),
        #    self._project_dir.file_list()
        # ))

    def diff_java_sources(self, rhs) -> FilesDiff:
        files_lhs = set(list(self.java_source_files))
        files_rhs = set(list(rhs.java_source_files))
        both = files_lhs & files_rhs
        return FilesDiff(
            both=sorted(list(both)),
            left_only=sorted(list(map(lambda x: os.path.join(
                self._project_dir.full_path, x), files_lhs - both))),
            right_only=sorted(list(map(lambda x: os.path.join(
                rhs._project_dir.full_path, x), files_rhs - both)))
        )
