class A!1:
    def __init__(self, a):
        self.a = None

class A!2:
    def __init__(self, a):
        self.a = None

class CmpChk!1:
    def check(self, s, t):
        return s

a1 = A!1()
a2 = A!2().incompatible(A, 2) # Aのバージョン2以外から作られた値と非互換な可能性がある値
b = CmpChk!1().check(a1, a2) # 意味的に非互換なバージョンから作られた値を混ぜて使用したことによるエラー
