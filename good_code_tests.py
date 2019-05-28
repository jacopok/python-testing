class parent:

    def __init__(self, **properties):

        for key, value in properties.items():
            setattr(parent, key, value)

class child(parent):

    def __init__(self, name, **properties):
        parent.__init__(self, **properties)
        self.name = name

    @staticmethod
    def multiply(f, g):
        return f*g

    def multiply_properties(self):
        return self.multiply(self.a, self.b)


y = child("Bob", a=20, b=10)

print(y.multiply_properties())
print(child.multiply(1, 2))
