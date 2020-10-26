
import numpy
import json
import os
import pwd
import datetime
import time
import weakref

from sys import byteorder
little = byteorder == 'little'

from bison import get_crc32, BisonError

__all__ = ['save','load']


def save(fname, *args):
    if os.path.isfile(fname):
        raise BisonError(f'[Bison]: File {fname} already exists')
    
    www = [pwd.getpwuid(os.getuid())[0], os.uname()[1], datetime.datetime.now().strftime('%c')]

    book = weakref.WeakValueDictionary()
    
    class Encoder(json.JSONEncoder):
        
        def _encode(self, data):

            if isinstance(data,tuple):
                return {'__tuple__': True, 'data': [self._encode(e) for e in data]}
            elif isinstance(data,list):
                return {'__list__': True, 'data': [self._encode(e) for e in data]}                
            elif isinstance(data,dict):
                return {key: self._encode(value) for key, value in data.items()}
            elif isinstance(data,numpy.ndarray):
                if little:
                    crc32 = get_crc32(data.tobytes("C"))
                else:
                    # array.byteswap changes byte order of underlying data
                    crc32 = get_crc32(data.byteswap().tobytes("C"))
                book[id(data)] = data
                return {'__numpy.ndarray__': True, 'crc32': crc32, 'shape': numpy.shape(data), 'dtype': data.dtype.str}
            elif isinstance(data,complex):
                return {'__complex__': True, 'data': [self._encode(data.real), self._encode(data.imag)]}
            else:
                return data

        def default(self, obj):
            if hasattr(obj,'__dict__'):
                tag = f'__{obj.__class__.__module__}.{obj.__class__.__name__}__'
                return {tag: self._encode(obj.__dict__)}
                
        def encode(self, obj):
            return super(Encoder, self).encode(self._encode(obj))

    header = Encoder(indent=2).encode({'www': www, 'data': list(args)})
    n = len(header)

    dt = -time.time()
    with open(fname, 'wb') as f:
        f.write(n.to_bytes(4, 'little'))
        f.write(str.encode(header))
        n += 4
        
        for key in book:
            array = book[key]
            n += array.nbytes
            if little:
                f.write(array.tobytes("C"))
            else:
                f.write(array.byteswap().tobytes("C"))
                
    dt += time.time()
    print(f'[Bison]: Written {n/1024.**2:g} MB at {n/1024.**2/dt:g} MB/s')
    

def load(fname, decoder=None):
    if not os.path.isfile(fname):
        raise BisonError(f'[Bison]: File {fname} does not exist')
    
    print(f'[Bison]: Reading file {fname}')
    dt = -time.time()
    
    if not decoder is None:
        if not type(decoder) is list:
            decoder = [decoder]
    
    with open(fname, 'rb') as f:
        n = int.from_bytes(f.read(4), 'little')
        header = f.read(n).decode('utf-8')
        nbytes = [4, n]
        
        def decode_hook(obj):
            if not decoder is None:
                for dec in decoder:
                    n = f'__{dec.type}__'
                    if n in obj:
                        return dec.decode(obj[n])
            
            if '__tuple__' in obj:
                return tuple(obj['data'])
            elif '__list__' in obj:
                return list(obj['data'])
            elif '__numpy.ndarray__' in obj:
                dt = numpy.dtype(obj['dtype'])
                sh = tuple(obj['shape'])
                sz = dt.itemsize * numpy.prod(sh)
                bb = f.read(sz)
                nbytes.append(sz)
                if get_crc32(bb)!=obj['crc32']:
                    raise BisonError(f'Checksum failed')
                if little:
                    return numpy.frombuffer(bb, dtype=dt).reshape(sh)
                else:
                    return numpy.frombuffer(bb, dtype=dt).byteswap().reshape(sh)
            elif '__complex__' in obj:
                return complex(*obj['data'])
            else:
                return obj
            
        res = json.loads(header, object_hook=decode_hook)
      
    dt += time.time()
    print(f'[Bison]: File created by {res["www"][0]} at {res["www"][1]} on {res["www"][2]}')
    print(f'[Bison]: Read {sum(nbytes)/1024.**2:g} MB at {sum(nbytes)/1024.**2/dt:g} MB/s')
    
    if len(res['data'])==1:
        return res['data'][0]
    return res['data']