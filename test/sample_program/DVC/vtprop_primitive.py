class A!1:
    def id(self, v):
        return v

class A!2:
    def id(self, v):
        return v

class B!1:
    def id(self, v):
        return v

a1 = A!1()
a2 = A!2()
b1 = B!1()

v_a1 = a1.id(1)
v_a2 = a2.id(1)
v_b1 = b1.id(1)

print(v_a1.vt) # 1
print(v_a2.vt) # 4
print(hasattr(v_b1, 'vt')) # False
print((v_a1 + v_a2).vt) # 5
print((v_a1 + v_b1).vt) # 1
print((v_b1 + v_a2).vt) # 4
print((v_a1 + v_a1).vt) # 1
