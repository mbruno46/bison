

__all__ = ['Decoder']

class Decoder:
    def __init__(self, t):
        self.type = t
        
    def decode(self, obj):
        return obj