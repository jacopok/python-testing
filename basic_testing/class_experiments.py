import math


class Circle():
    'Docstring here'

    version = '0.1'

    __slots__ = ['diameter']

    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        p = self.__perimeter
        r = p / math.pi / 2.

        return math.pi * r**2

    @property
    def perimeter(self):
        return 2. * math.pi * self.radius

    __perimeter = perimeter

    @property
    def radius(self):
        return self.diameter / 2.

    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.

    @classmethod
    def from_bbd(cls, bbd):
        radius = bbd / math.sqrt(2.) / 2
        return cls(radius)

    @staticmethod
    def degrees_to_radians(angle_degrees):
        return angle_degrees / 180. * math.pi


class Tire(Circle):

    multiplier = 1.25

    @property
    def perimeter(self):
        return super().perimeter * Tire.multiplier


class FixedAreaPrism():
    
    def __init__(self, base_area, height):
        self.base_area = base_area
        self.height = height
    
    @property
    def volume(self):
        return self.base_area * self.height
    

class Cylinder(Circle, FixedAreaPrism):
    
    def __init__(self, radius, height):
        Circle.__init__(self, radius)
        FixedAreaPrism.__init__(self, self.area, height)
    