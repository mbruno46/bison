
import zlib
from sys import byteorder
little = byteorder == 'little'

def get_crc32(b):
    return f'{zlib.crc32(b):8X}'

class BisonError(Exception):
    pass

from .io import *
from .decoder import Decoder

__all__ = ['get_crc32','BisonError']
__all__.extend(io.__all__)
__all__.extend(decoder.__all__)
