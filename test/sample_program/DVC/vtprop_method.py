class A!1:
    pass

class A!2:
    def inc(self, v):
        return v + 1

class B!1:
    def inc(self, v):
        return v + 1

a2 = A!2()
b1 = B!1()
n = 1
return_value_from_a2 = a2.inc(n)
return_value_from_b1 = b1.inc(n)
print(hasattr(n, 'vt')) # False
print(return_value_from_a2.vt) # 0100 -> 4
print(hasattr(return_value_from_b1, 'vt')) # False
