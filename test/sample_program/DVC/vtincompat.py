class A!1:
    def id(self, v):
        return v

class A!2:
    def id(self, v):
        result = v + 1
        return _incompatible_value(result, "A", 2, "incompatibly updated")

class B!1:
    def id(self, v):
        return v
    
a2 = A!2()
print(a2.vt) # 0100 -> 4
print(a2.id(1).vt) # 1100 -> 12