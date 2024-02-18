class Hash!1:
    def __init__(self):
        pass

    def compute(self, a):
        return a.firstCharCode().increment()

class Hash!2:
    def __init__(self):
        pass

    def compute(self, a):
        return a.firstCharCode().decrement().incompatible(Hash, 2)
    
class Equal!1:
    def __init__(self):
        pass
    def equal(self, a, b):
        return self

class String!1:
    def __init__(self, c):
        self.first = c
    def firstCharCode(self):
        return self.first

class Char!1:
    def __init__(self):
        pass
    def increment(self):
        return Char!1()
    def decrement(self):
        return Char!1()

h1 = Hash!1()
h2 = Hash!2()

a = Char!1()
b = Char!1()

s1 = String!1(a)
s2 = String!1(b)

Equal!1().equal(h1.compute(s1), h2.compute(s2))

