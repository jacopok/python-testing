import unittest
from good_code_tests import child, parent

class TestChild(unittest.TestCase):

    def setUp(self):
        self.attr_list = ['a', 'b', 'first', 'second', 'third']
        self.value_list = [1, 2, 3, 4, 5]

        self.x = child('Bob')

        for name, value in zip(self.attr_list, self.value_list):
            setattr(self.x, name, value)

    def tearDown(self):
        pass

    def test_child(self):
        self.assertEqual(self.x.name, 'Bob', 'Wrong name')
        for attr_name, value in zip(self.attr_list, self.value_list):
            self.assertEqual(getattr(self.x, attr_name), value, 'wrong attribute')

    def test_child_creation(self):
        c = child.create_child()
        self.assertEqual(c.a, 1, 'message')

    def test_static_method(self):
        self.assertEqual(child.multiply(0,1), 0, 'staticmethod not working')
        self.assertEqual(child.multiply(10,-5), -50, 'staticmethod not working')

    def test_multiply_properties(self):
        self.assertEqual(self.x.multiply_properties(), 2, 'multiply_properties not working')
        c = child.create_child()
        self.assertEqual(c.multiply_properties(), 1, 'multiply_properties not working')

class TestParent(unittest.TestCase):

    def test_parent(self):
        x = parent(a=1)
        self.assertEqual(x.a, 1, 'message')

if __name__ == '__main__':
    unittest.main()
