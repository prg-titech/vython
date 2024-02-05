class C!1:
    def __init__(self):
        pass

    def id(self, a):
        return a

class D!1:
    def __init__(self):
        pass

c = C!1().id(D!1())
c
