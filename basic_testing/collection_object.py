from dataclasses import dataclass

@dataclass
class SmallClass():

    __slots__ = ('a',)
    a: float


@dataclass
class BiggerClass():
    
    __slots__ = ('a', 'b', 'c')
    
    b: float
    c: SmallClass


class ObjectList(list):
    def __getattr__(self, name):
        return self.__class__([getattr(obj, name) for obj in self])


if __name__ == "__main__":
    c1 = BiggerClass(b=0, c=SmallClass(1))
    c2 = BiggerClass(b=2, c=SmallClass(3))
    
    coll = ObjectList([c1, c2])
    
    print(coll.b)
    print(coll.c)
    print(coll.c.a)