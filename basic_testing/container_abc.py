
from collections.abc import MutableMapping


class WavelengthMap(MutableMapping):
    """Mutable mapping which rounds its keys.
    """
    
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.precision = kwargs.pop('precision', 4)
        self.data.update(*args)

    def _round(self, key):
        return(round(key, self.precision))

    def __getitem__(self, key):
        return self.data.__getitem__(self._round(key))
    
    def __setitem__(self, key, val):
        self.data.__setitem__(self._round(key), val)
        
    def __delitem__(self, key):
        self.data.__delitem__(self._round(key))
        
    def __iter__(self, key):
        return iter(self.data)
        
    def __len__(self, key):
        return len(self.data)
        
    def __repr__(self):
        return f'WavelengthMap({self.data!r}, precision={self.precision})'