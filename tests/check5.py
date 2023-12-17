import bison
import numpy
import os

alist = [4,5,(6,),[8,9+3j]]
array = numpy.arange(32**4).astype('i4')
astr = 'hello there'

f = bison.FILE('test', mode='w')
for k, field in enumerate([alist, array, astr]):
    f.write(f'tag{k}', field)

ff = bison.FILE('test', mode='a')
ff.write('New Tag', 'I have been appended')

f.close()

fff = bison.load('test')
assert fff['New Tag'] == 'I have been appended'