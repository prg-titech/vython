class Vector2!1:
    def __init__(self, n1, n2):
        self.n1 = n1
        self.n2 = n2

class Matrix2!1:
    def __init__(self, v1, v2):
        self.a11 = v1.n1
        self.a12 = v1.n2
        self.a21 = v2.n1
        self.a22 = v2.n2
    
    def matmul(self, other):
        tl = self.a11 * other.a11 + self.a12 * other.a21
        tr = self.a11 * other.a12 + self.a12 * other.a22
        bl = self.a21 * other.a11 + self.a22 * other.a21
        br = self.a21 * other.a12 + self.a22 * other.a22
        result = Matrix2!1(Vector2!1(tl,tr), Vector2!1(bl, br))
        return  result
    
v1 = Vector2!1(3,1)
v2 = Vector2!1(2,4)
v3 = Vector2!1(1,0)
v4 = Vector2!1(5,2)
m1 = Matrix2!1(v1,v2)
m2 = Matrix2!1(v3,v4)
m = m1.matmul(m2)
print(m.a11)
print(m.a12)
print(m.a21)
print(m.a22)

