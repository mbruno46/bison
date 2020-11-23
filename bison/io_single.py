#################################################################################
#
# io_single.py
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

import json
import os
import pwd
import datetime
import time
import bison

__all__ = ['save','load']


def save(fname, *args):
    if os.path.isfile(fname):
        raise bison.BisonError(f'File {fname} already exists')
    
    www = [pwd.getpwuid(os.getuid())[0], os.uname()[1], datetime.datetime.now().strftime('%c')]

    enc = bison.encoder.Encoder(indent=2)
    header = enc.encode({'www': www, 'data': list(args)})
    
    n = len(header)

    dt = -time.time()
    with open(fname, 'wb') as f:
        f.write(n.to_bytes(4, 'little'))
        f.write(str.encode(header))
        n += 4
        
        for key in enc.book:
            array = enc.book[key]
            n += array.nbytes
            if bison.little:
                f.write(array.tobytes("C"))
            else:
                f.write(array.byteswap().tobytes("C"))
            
    dt += time.time()
    bison.message(f'Written {n/1024.**2:g} MB at {n/1024.**2/dt:g} MB/s')
    

def load(fname, decoder=None):
    if not os.path.isfile(fname):
        raise bison.BisonError(f'File {fname} does not exist')
    
    bison.message(f'Reading file {fname}')
    dt = -time.time()
    
    dec = bison.Decoder(decoder)
    
    with open(fname, 'rb') as f:
        n = int.from_bytes(f.read(4), 'little')
        header = f.read(n).decode('utf-8')
        nbytes = [4, n]
        
        #res = json.loads(header, object_hook=bison.decoder.decode_hook)
        dec.set_file(f)
        res = json.loads(header, object_hook=dec.decode_hook)
        nbytes += dec.nbytes
        
    dt += time.time()
    bison.message(f'File created by {res["www"][0]} at {res["www"][1]} on {res["www"][2]}')
    bison.message(f'Read {sum(nbytes)/1024.**2:g} MB at {sum(nbytes)/1024.**2/dt:g} MB/s')
    
    if len(res['data'])==1:
        return res['data'][0]
    return res['data']