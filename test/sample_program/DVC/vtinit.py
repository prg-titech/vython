class A!1:
    pass

class A!2:
    pass

class B!1:
    pass

a1 = A!1()
a2 = A!2()
b1 = B!1()
print(a1.vt) # 0001 -> 1
print(a2.vt) # 0100 -> 4
print(hasattr(b1, 'vt')) # False
