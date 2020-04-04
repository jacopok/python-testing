import math


class Circle():
    'Docstring here'

    version = '0.1'
    
    __slots__ = ['diameter']

    def __init__(self, radius):
        self.radius = radius 

    def area(self):
        p = self.__perimeter()
        r = p / math.pi / 2.

        return math.pi * r**2

    def perimeter(self):
        return 2. * math.pi * self.radius
    
    __perimeter = perimeter
    
    @property
    def radius(self):
        return self.diameter / 2.
    
    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.
    
    # @property
    # def diameter(self):
    #     return self.diameter 
    
    # @diameter.setter
    # def diameter(self, diameter):
    #     self.diameter = diameter

    @classmethod 
    def from_bbd(cls, bbd):
        radius = bbd / math.sqrt(2.) / 2
        return cls(radius)


class Tire(Circle):
    
    multiplier = 1.25
    
    def perimeter(self):
        return super.__perimeter(self) * Tire.multiplier
        