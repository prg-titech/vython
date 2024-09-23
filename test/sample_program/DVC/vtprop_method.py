class A!1:
    pass

class A!2:
    def id(self, v):
        return v

class B!1:
    def id(self, v):
        return v

a2 = A!2()
b1 = B!1()
num = 1
print(hasattr(num, 'vt')) # False
print(a2.vt) # 0100 -> 4
print(a2.id(num).vt) # 0100 -> 4
print(hasattr(b1.id(num), 'vt')) # False
