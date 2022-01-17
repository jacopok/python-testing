from typing import Optional

class C:
    
    def __init__(self):
        self.a : Optional[int]
    
    @property
    def a_is_not_none(self) -> bool:
        return self.a is not None
    
    def one_plus_a(self) -> int:
        assert self.a_is_not_none
        return self.a + 1
        
        
"""
This code does not work! 
"""