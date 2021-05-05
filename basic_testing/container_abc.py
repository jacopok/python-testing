
from collections.abc import MutableMapping


class WavelengthMap(MutableMapping):
    """Mutable mapping which rounds its keys.
    """
    
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.precision = kwargs.pop('precision', 4)
        self.data.update(*args, **kwargs)

    def _round(self, key):
        return(round(key, self.precision))

    def __getitem__(self, key):
        return self.data.__getitem__(self._round(key))
    
    def __setitem__(self, key, val):
        self.data.__setitem__(self._round(key), val)
        
    def __delitem__(self, key):
        self.data.__delitem__(self._round(key))
        
    def __iter__(self):
        return iter(self.data)
        
    def __len__(self, key):
        return len(self.data)
        
    def __repr__(self):
        return f'WavelengthMap({self.data!r}, precision={self.precision})'

from functools import wraps

def delayed_init_wrapper(func):
    def delayed_constructor(*args, **kwargs):
        
        
        
        return func(*args, **kwargs)
    
    return delayed_constructor

from time import sleep

class HeavyClass():

    def __init__(self, data):
        print("doin' lots of stuff")
        sleep(1)
        self.data = data
        print('done')
    
    @classmethod
    def create(cls):
        return cls((1, 2, 3))


class HeavyClass2():

    def __new__(cls, *args, **kwargs):
        print('__new__ called!')
        return super().__new__(cls)

    def __init__(self, data):
        print("doin' lots of stuff")
        sleep(1)
        self.data = data
        print('done')
    
    @classmethod
    @delayed_init_wrapper
    def create(cls):
        return cls((1, 2, 3))
