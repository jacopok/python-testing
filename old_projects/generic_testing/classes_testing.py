class Circle:

    def __init__(self, radius=1):
        self.radius = radius

    @property
    def area(self):
        from math import pi
        print('Calculating area...')
        return self.radius**2 * pi

    @area.setter
    def area(self, area):
        from math import sqrt, pi
        print('Calculating radius...')
        self.radius = sqrt(area / pi)