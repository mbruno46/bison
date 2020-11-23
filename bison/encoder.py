#################################################################################
#
# encoder.py
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
import json
import weakref

from bison import get_crc32, little

class Encoder(json.JSONEncoder):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        #super(Encoder, self).__init__()
        self.book = weakref.WeakValueDictionary()
        
    def _encode(self, data):
        if hasattr(data,'__dict__'):
            tag = f'__{data.__class__.__module__}.{data.__class__.__name__}__'
            return {tag: self._encode(data.__dict__)}

        if isinstance(data,tuple):
            return {'__tuple__': True, 'data': [self._encode(e) for e in data]}
        elif isinstance(data,list):
            return {'__list__': True, 'data': [self._encode(e) for e in data]}                
        elif isinstance(data,dict):
            return {key: self._encode(value) for key, value in data.items()}
        elif isinstance(data,range):
            return {'__range__': True, 'data': [data.start, data.stop, data.step]}
        elif isinstance(data,numpy.ndarray):
            if little:
                crc32 = get_crc32(data.tobytes("C"))
            else:
                # array.byteswap changes byte order of underlying data
                crc32 = get_crc32(data.byteswap().tobytes("C"))
            self.book[id(data)] = data
            return {'__numpy.ndarray__': True, 'crc32': crc32, 'shape': numpy.shape(data), 'dtype': data.dtype.str}
        elif isinstance(data,(complex)):
            return {'__complex__': True, 'data': [self._encode(data.real), self._encode(data.imag)]}
        else:
            if isinstance(data,(numpy.int32,numpy.int64)):
                return int(data)
            return data


    def encode(self, obj):
        return super(Encoder, self).encode(self._encode(obj))
