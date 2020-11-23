#################################################################################
#
# decoder.py
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

import numpy
import bison

__all__ = ['Decoder']


class Decoder:
    def __init__(self, decoder, tags=None):
        if not decoder is None:
            if not type(decoder) is list:
                self.decoder = [decoder()]
            else:
                self.decoder = [d() for d in decoder]
        else:
            self.decoder = []
        self.nbytes = []
            
    def set_file(self, f):
        self.f = f
        
    def decode_hook(self,obj):
        if self.decoder:
            for dec in self.decoder:
                n = f'__{dec.type}__'
                if n in obj:
                    return dec.decode(obj[n])
        
        if '__tuple__' in obj:
            return tuple(obj['data'])
        elif '__list__' in obj:
            return list(obj['data'])
        elif '__range__' in obj:
            return range(*obj['data'])
        elif '__numpy.ndarray__' in obj:
            dt = numpy.dtype(obj['dtype'])
            sh = tuple(obj['shape'])
            sz = dt.itemsize * numpy.prod(sh)
            bb = self.f.read(sz)
            self.nbytes.append(sz)
            if bison.get_crc32(bb)!=obj['crc32']: # pragma: no cover
                raise bison.BisonError(f'Checksum failed')
            if bison.little:
                return numpy.frombuffer(bb, dtype=dt).reshape(sh)
            else:
                return numpy.frombuffer(bb, dtype=dt).byteswap().reshape(sh)
        elif '__complex__' in obj:
            return complex(*obj['data'])
        else:
            return obj
        
