class A!1:
    def id(self, v):
        return v

class A!2:
    def id(self, v):
        return v

class B!1:
    def id(self, v):
        return v
    def inc(self, v):
        return v + 1
    
class B!2:
    def id(self, v):
        return v
    def inc(self, v):
        result = v + 2
        return _incompatible_value(result, "B", 2, "incompatibly updated")

b1 = B!1().id(1) # 00010000 -> 16
b2 = B!2().id(1) # 01000000 -> 64
bi1 = B!1().inc(1) # 00010000 -> 16
bi2 = B!2().inc(2) # 110000 -> 192
bi1 + bi2 # VersionError
