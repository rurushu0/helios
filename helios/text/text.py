from enum import Enum
from helios.core import classproperty


class Encoding(Enum):
    SJIS = 'CP932'
    UTF8 = 'utf-8'

    @classproperty
    def __values__(cls):
        return [
            Encoding.UTF8.value,
            Encoding.SJIS.value
        ]
