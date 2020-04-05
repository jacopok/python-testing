import unittest
from class_experiments import Circle, Tire, Cylinder
import math


class TestCircle(unittest.TestCase):

    radius_value = 10.

    def test_radius(self):
        c = Circle(self.radius_value)
        self.assertAlmostEqual(c.radius, self.radius_value)

    def test_diameter(self):
        c = Circle(self.radius_value)
        self.assertAlmostEqual(c.diameter, self.radius_value * 2.)
        self.assertAlmostEqual(c.diameter, c.radius * 2.)

    def test_area(self):
        c = Circle(self.radius_value)
        self.assertAlmostEqual(c.area, math.pi * c.radius**2.)

    def test_perimeter(self):
        c = Circle(self.radius_value)
        self.assertAlmostEqual(c.perimeter, 2. * math.pi * c.radius)

    def test_conversion_degrees_to_radians(self):
        angle_deg = 30.
        angle_rad = math.pi / 6.
        self.assertAlmostEqual(Circle.degrees_to_radians(angle_deg), angle_rad)

    def test_construction_from_bbd(self):
        bbd = math.sqrt(2.) * 2.
        radius = 1.
        c = Circle.from_bbd(bbd)
        self.assertAlmostEqual(c.radius, radius)


class TestTire(unittest.TestCase):

    radius_value = 10.

    def test_perimeter(self):
        t = Tire(self.radius_value)
        self.assertAlmostEqual(t.perimeter,
                               t.radius * Tire.multiplier * math.pi * 2.)


class TestCylinder(unittest.TestCase):

    radius = 10.
    height = 10.

    def test_volume(self):
        c = Cylinder(self.radius, self.height)
        self.assertAlmostEqual(c.volume,
                               math.pi * self.radius**2 * self.height)
        self.assertAlmostEqual(c.area, math.pi * self.radius**2)


if __name__ == '__main__':
    unittest.main()