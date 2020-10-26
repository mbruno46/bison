import bison
import numpy
import os

alist = [4,5,(6,),[8,9+3j]]
atuple = (4,5,(6,))
array = numpy.arange(32**4).astype('i4')
astr = 'hello there'
afl = 3.14
numpys = [numpy.int32(32), numpy.int64(64)]

bison.save('test1',alist, atuple, atuple, array, astr, afl, numpys)

res = bison.load('test1')

assert (alist == res[0])
assert (atuple == res[1])
assert (atuple == res[2])
assert numpy.all(array == res[3])
assert (astr == res[4])
assert (afl == res[5])
assert numpy.all(numpys == res[6])

try:
    bison.save('test1')
except bison.BisonError:
    print('error caugth')

try:
    bison.load('test22')
except bison.BisonError:
    print('error caugth')

os.popen('rm test1')
