class A!1():
    def __init__(self):
        pass

    def add(self, v1, v2):
        result = v1 + v2
        return result
    
class A!2():
    def __init__(self):
        pass

    def add(self, v1, v2):
        result = v1 + v2 + 1
        return _incompatible_value(result, "A", 2)
    
class B!1():
    def add(self, v1,v2):
        return v1 + v2
    
class B!2():
    def add(self, v1,v2):
        return v1 + v2


a1 = A!1()
a2 = A!2()

v1 = a1.add(1,2)
v2 = a2.add(1,2)

print(v1 == v2)

