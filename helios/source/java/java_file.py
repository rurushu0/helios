from helios.file import File
import javaproperties


class JavaSourceFile(File):
    def __init__(self, file_path):
        super().__init__(file_path)
        with open(file_path, 'r', encoding=self.encoding.value) as fp:
            self._properties = javaproperties.load(fp)

    @property
    def properties(self) -> dict:
        return self._properties


# import subprocess
# subprocess.call(['java', '-jar', 'Blender.jar'])
