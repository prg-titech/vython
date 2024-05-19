class A!1:
    def __init__(self, a):
        self.a = None

class A!2:
    def __init__(self, a):
        self.a = None

class CmpChk!1:
    def check(self, s, t):
        return s

a1 = A!2()
a2 = A!2().incompatible(A, 2)
CmpChk!1().check(a1, a2) # 意味的に互換なバージョンから作られた値の計算なので実行可能
