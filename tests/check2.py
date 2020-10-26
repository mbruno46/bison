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
        
    def __call__(self):
        return numpy.sum(self.b.data)
    
aclass = A(45)
aclass2 = A(100)

bison.save('test',aclass, aclass2)

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


res = bison.load('test',decoder = [Adec(), Bdec()])

assert (res[0].n == aclass.n)
assert (res[0].name == aclass.name)
assert numpy.all(res[0].b.data == aclass.b.data)

assert (res[1].n == aclass2.n)
assert (res[1].name == aclass2.name)
assert numpy.all(res[1].b.data == aclass2.b.data)

os.popen('rm test')