class A!1:
    pass

class A!2:
    def id(self, v):
        return v

a2 = A!2()
n = 1
return_value_from_a2 = a2.id(n)

print(a2.vt)
print(return_value_from_a2.vt)
print(n.vt) # オブジェクトがそのまま帰ってくるので、nから参照できるオブジェクトにもvtが付いている。
