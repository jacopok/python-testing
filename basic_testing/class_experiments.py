import math


class Circle():
    # 'Docstring here'

    # version = '0.1'

    __slots__ = 'diameter', '_perimeter', '_radius'

    def __init__(self, radius):
        self._radius = radius
        self._perimeter = None

    @property
    def area(self):
        p = self.perimeter
        r = p / math.pi / 2.

        return math.pi * r**2

    @property
    def perimeter(self):
        if self._perimeter is None:
            print('Calculating perimeter!')
            self._perimeter = 2. * math.pi * self.radius

        return self._perimeter


    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        self.diameter = radius * 2.
        self._radius = radius

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
    
    
