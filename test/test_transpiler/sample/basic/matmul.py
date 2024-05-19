class Mat!1:
    def __init__(self, n1, n2, n3):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

    def matmul(self, other):
        return self.n1 * other.n1 + self.n2 * other.n2 + self.n3 * other.n3
    

m1 = Mat!1(1,4,6)
m2 = Mat!1(3,7,8)
print(m1.matmul(m2))

