from enum import Enum
from helios.core import classproperty


class Encoding(Enum):
    ASCII = 'ascii'
    UTF8 = 'utf-8'
    SJIS = 'CP932'

    @classproperty
    def __values__(cls):
        return [
            Encoding.ASCII.value,
            Encoding.UTF8.value,
            Encoding.SJIS.value
        ]
