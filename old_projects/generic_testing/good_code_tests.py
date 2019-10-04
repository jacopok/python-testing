class parent:

    def __init__(self, **properties):

        for key, value in properties.items():
            setattr(parent, key, value)

class child(parent):

    def __init__(self, name, **properties):
        parent.__init__(self, **properties)
        self.name = name

    @classmethod
    def create_child(cls):
        return cls('Bob', a=1, b=1)

    @staticmethod
    def multiply(f, g):
        return f*g

    def multiply_properties(self):
        return self.multiply(self.a, self.b)

if(__name__ == '__main__'):
    y = child("Bob", a=20, b=10)
    print(y.multiply_properties())
    print(child.multiply(1, 2))
    x = child.create_child()
    print(x.multiply_properties())
