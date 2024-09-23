class A!1:
    def id(self, v):
        return v
    def inc(self, v):
        return v + 1

class A!2:
    def id(self, v):
        return v
    def inc(self, v):
        result = v + 2
        return _incompatible_value(result, "A", 2, "incompatibly updated")

class B!1:
    def id(self, v):
        return v
    
class B!2:
    def id(self, v):
        return v
    
a1 = A!1().id(1) # 00000001 -> 1
a2 = A!2().id(1) # 00000100 -> 4
b1 = B!1().id(1) # 00010000 -> 16
b2 = B!2().id(1) # 01000000 -> 64
ai1 = A!1().inc(1) # 00000001 -> 1
ai2 = A!2().inc(2) # 00001100 -> 12
print((a1 + b1 + b2).vt) # 01010001 -> 81
print((a2 + b2).vt) # 01000100 -> 68

print((ai2 + b1).vt) # 00011100 -> 28
