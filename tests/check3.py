import bison
import numpy
import os

alist = [4,5,(6,),[8,9+3j]]
atuple = (4,5,(6,))
array = numpy.arange(32**4).astype('i4')
astr = 'hello there'
afl = 3.14
arange = range(4,127,3)
numpys = [numpy.int32(32), numpy.int64(64)]

all = [alist, atuple, atuple, array, astr, afl, arange, numpys]
f = bison.FILE('test3', mode='w')
k = 0
for field in all:
    f.write(f'tag{k}', field)
    k+=1

f.close(dest='test33')

f2 = bison.FILE('test3', mode='r')
res = f2.read()

k=0
for field in all:
    assert numpy.all(field == res[f'tag{k}'])
    k+=1

try:
    bison.FILE('test3', mode='w')
except bison.BisonError:
    print('error caugth')

try:
    bison.FILE('test333', mode='r')
except bison.BisonError:
    print('error caugth')

try:
    bison.FILE('test333', mode='read')
except bison.BisonError:
    print('error caugth')

try:
    f.read()
except bison.BisonError:
    print('error caugth')    

try:
    f2.write('pi',3.14)
except bison.BisonError:
    print('error caugth')    

f.close()
f2.close()

os.popen('rm test3 test33')
