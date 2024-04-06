class A!1:
    def __init__(self, a):
        self.n = a

    def getN(self):
        return self.n

class A!2:
    def __init__(self, b):
        self.n = b

    def getN(self):
        return self.n.incompatible(A, 2)

a = A!1(2)
b = A!2(5)

a.getN() + b.getN()

