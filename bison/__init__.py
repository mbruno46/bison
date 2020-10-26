
import zlib
from sys import byteorder
little = byteorder == 'little'

def get_crc32(b):
    return f'{zlib.crc32(b):8X}'

class BisonError(Exception):
    pass

__all__ = ['get_crc32','BisonError']

from .io import *
__all__.extend(io.__all__)

from .decoder import Decoder
__all__.extend(decoder.__all__)

from .version import __version__, __version_full__
__all__.extend(['__version__'])
