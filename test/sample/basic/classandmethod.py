class C!1:
    def __init__(self):
        pass

    def id(self, a):
        return a
    
    def id1(self, a):
        return self.id(a)

class D!1:
    def __init__(self):
        pass

c = C!1().id1(D!1())
c
