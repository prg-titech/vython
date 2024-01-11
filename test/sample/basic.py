class C:
    def __init__(self):
        pass

    def id(self, a):
        return a


class D:
    def __init__(self):
        pass


c = C().id(D())
d = D()
c
