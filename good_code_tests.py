class parent():

    def __init__(self, **properties):

        for key, value in properties.items():
            setattr(parent, key, value)

class child(parent):

    def __init__(self, name, **properties):
        parent.__init__(**properties)
        self.name = name

x = parent(a = 10)

print(x.a)

y = child("Bob", a=20)

y.
