class Hash!1:
    def __init__(self):
        pass

    def hash(self, a):
        return a

class Hash!2:
    def __init__(self):
        pass

    def hash(self, a):
        return a.incompatible(Hash, 2)
    
class Equal!1:
    def __init__(self):
        pass
    def equal(self, a, b):
        return self

class String!1():
    def __init__(self):
        pass
    
h1 = Hash!1()
h2 = Hash!2()

s1 = String!1()
s2 = String!1()

Equal!1().equal(h1.hash(s1), h2.hash(s2))

