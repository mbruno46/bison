import bison
import numpy
import os

class B:
    def __init__(self,n):
        self.data = numpy.arange(n).astype('i4')
        
class A:
    def __init__(self,n):
        self.n = n
        self.name = 'a class'
        self.b = B(self.n)
        self.data0 = numpy.random.rand(4)
        
    def __call__(self):
        return numpy.sum(self.b.data)
    
aclass = A(45)
array = numpy.random.rand(128)

bison.save('test',aclass, array)

res1 = bison.load('test')
print('Reading a class without decoder', res1)


class Adec(bison.Decoder):
    def __init__(self):
        super().__init__('__main__.A')
        
    def decode(self, obj):
        out = A(obj['n'])
        return out

class Bdec(bison.Decoder):
    def __init__(self):
        super().__init__('__main__.B')
        
    def decode(self, obj):
        out = B(len(obj['data']))
        out.data = obj['data']
        return out


res2 = bison.load('test',decoder = [Adec, Bdec])

assert (res2[0].n == aclass.n)
assert (res2[0].name == aclass.name)
assert numpy.all(res2[0].b.data == aclass.b.data)

assert numpy.all(res2[1] == array)

bison.save('class', aclass)

class empty_dec(bison.Decoder):
    def __init__(self):
        super().__init__('__main__.A')
        
res3 = bison.load('class', decoder=empty_dec)

os.popen('rm test class')