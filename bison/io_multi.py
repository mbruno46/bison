#################################################################################
#
# io_multi.py
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
import os
import pwd
import datetime
import time
import weakref

import bison

__all__ = ['FILE']

def strip(string):
    return string[2:-2]

class FILE:
    def __init__(self, fname, mode):
        self.fname = fname
        self.path = f'{fname}.temp'
        self.head = f'{self.path}/head'
        self.data = f'{self.path}/data'
        
        if mode == 'r':
            self.reading = True
            if not os.path.isfile(self.head) and not os.path.isfile(self.fname):
                raise bison.BisonError(f'File {fname} does not exist')
        elif mode == 'w':
            self.reading = False
            if os.path.isfile(self.head) or os.path.isfile(self.data) or os.path.isfile(self.fname):
                raise bison.BisonError(f'File {fname} already exists')
            else:
                os.makedirs(self.path, exist_ok=True)
            
            enc = bison.encoder.Encoder(indent=0)
            www = [pwd.getpwuid(os.getuid())[0], os.uname()[1], datetime.datetime.now().strftime('%c')]
        
            # init header file
            header = strip(enc.encode({'www': www, 'data': {}}))
            with open(self.head, 'w') as f:
                f.write(header[:-1] + '\n')
            
            self.tags = ['www']
        else:
            raise bison.BisonError(f'Unexpected mode')

    
    def write(self, tag, data):
        if self.reading:
            raise bison.BisonError(f'File opened in read mode')
            
        if tag in self.tags:
            raise bison.BisonError(f'Tag {tag} already used')
        
        enc = bison.encoder.Encoder(indent=0)

        header = strip(enc.encode({tag: data}))
        n = len(header)
        
        dt = -time.time()
        with open(self.head, 'a') as f:
            f.write(header+',\n')
        
        if len(enc.book)>0:
            with open(self.data, 'ab') as f:
                for key in enc.book:
                    array = enc.book[key]
                    n += array.nbytes
                    if bison.little:
                        f.write(array.tobytes("C"))
                    else:
                        f.write(array.byteswap().tobytes("C"))
            
        dt += time.time()
        bison.message(f'{tag} with {n/1024.**2:g} MB written at {n/1024.**2/dt:g} MB/s')

    
    def read(self, decoder=None):
        if not self.reading:
            raise bison.BisonError(f'File opened in write mode')
            
        bison.message(f'Reading file {self.fname}')
        dt = -time.time()
        
        dec = bison.Decoder(decoder)

        if os.path.isfile(self.fname):
            f = open(self.fname, 'rb')
            n = int.from_bytes(f.read(4), 'little')
            header = f.read(n).decode('utf-8')
            
            nbytes = [4, n]
            dec.set_file(f)
        elif os.path.isfile(self.head):
            header = '{\n' + open(self.head, 'r').read()[:-2] + '\n}\n}'
            nbytes = [len(header)]
        
            if os.path.isfile(self.data):
                f = open(self.data, 'rb')
                dec.set_file(f)
            
        res = json.loads(header, object_hook=dec.decode_hook)
        nbytes += dec.nbytes
        
        dt += time.time()
        
        bison.message(f'File created by {res["www"][0]} at {res["www"][1]} on {res["www"][2]}')
        bison.message(f'Read {sum(nbytes)/1024.**2:g} MB at {sum(nbytes)/1024.**2/dt:g} MB/s')
        
        return res['data']
    

    def close(self, dest=None):
        if self.reading:
            pass
        
        header = '{\n' + open(self.head, 'r').read()[:-2] + '\n}\n}'
        n = len(header)
        
        if dest is None:
            dst = self.fname
        else:
            dst = dest
            
        with open(dst, 'wb') as f:
            f.write(n.to_bytes(4, 'little'))
            f.write(str.encode(header))
            n += 4
           
            if os.path.isfile(self.data):
                bb = open(self.data, 'rb').read()
                n += len(bb)
                f.write(bb)
        
        os.popen(f'rm -r {self.path}')