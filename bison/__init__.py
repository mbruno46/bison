#################################################################################
#
# __init__.py
# Copyright (C) 2020 Mattia Bruno
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#################################################################################

import zlib
from sys import byteorder
little = byteorder == 'little'

def get_crc32(b):
    return f'{zlib.crc32(b):8X}'

class BisonError(Exception):
    pass

verbose = True

def message(msg):
    if verbose:
        print(f'[Bison] : {msg}')

__all__ = ['get_crc32','BisonError']

from .encoder import Encoder

from .decoder import Decoder
__all__.extend(decoder.__all__)

from .version import __version__, __version_full__
__all__.extend(['__version__'])

from .io_single import *
__all__.extend(io_single.__all__)

from .io_multi import *
__all__.extend(io_multi.__all__)