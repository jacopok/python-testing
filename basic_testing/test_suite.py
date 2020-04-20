import unittest
from class_experiments import Circle, Tire, Cylinder
import math
from hypothesis import given
import hypothesis.strategies as st

FLOAT_OPTIONS = {'min_value': 0, 'max_value': 1e30, 'allow_nan': False}


class TestCircle(unittest.TestCase):
    @given(st.floats(**FLOAT_OPTIONS))
    def test_radius(self, r):
        c = Circle(r)
        self.assertAlmostEqual(c.radius, r)

    @given(st.floats(**FLOAT_OPTIONS))
    def test_diameter(self, r):
        c = Circle(r)
        self.assertAlmostEqual(c.diameter, r * 2.)
        self.assertAlmostEqual(c.diameter, c.radius * 2.)

    @given(st.floats(**FLOAT_OPTIONS))
    def test_area(self, r):
        c = Circle(r)
        self.assertTrue(
            math.isclose(c.area, math.pi * c.radius**2., rel_tol=1e-9))

    @given(st.floats(**FLOAT_OPTIONS))
    def test_perimeter(self, r):
        c = Circle(r)
        self.assertAlmostEqual(c.perimeter, 2. * math.pi * c.radius)

    @given(st.floats(**FLOAT_OPTIONS))
    def test_conversion_degrees_to_radians(self, angle_deg):
        angle_rad = angle_deg * math.pi / 180.
        self.assertTrue(
            math.isclose(Circle.degrees_to_radians(angle_deg), angle_rad))

    @given(st.floats(**FLOAT_OPTIONS))
    def test_construction_from_bbd(self, r):
        bbd = math.sqrt(2.) * 2. * r
        c = Circle.from_bbd(bbd)
        self.assertTrue(math.isclose(c.radius, r, rel_tol=1e-9))


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