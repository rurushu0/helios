from enum import Enum
from helios.core import classproperty


class Encoding(Enum):
    ASCII = 'ascii'
    UTF8 = 'utf-8'
    UTF8_SIG = 'UTF-8-SIG'
    SJIS = 'CP932'
    CP1252 = "Windows-1252"

    @classproperty
    def __values__(cls):
        return [
            Encoding.ASCII.value,
            Encoding.UTF8.value,
            Encoding.SJIS.value,
            Encoding.CP1252.value,
            Encoding.UTF8_SIG.value
        ]
