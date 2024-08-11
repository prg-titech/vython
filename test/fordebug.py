# クラス定義
class Calculator!2:
    def __init__(self):
        self.result = 0

    def add(self, value):
        self.result = self.result + value

    def subtract(self, value):
        self.result = self.result - value

    def getResult(self):
        return self.result
    
class Calculator!3():
    def add(self):
        return
    
class AAA!3():
    def add(self):
        return
    
class AAA!4():
    def add(self):
        return

# クラスのインスタンス生成とメソッド呼び出し
calc = Calculator!2()
calc.add(10)
calc.subtract(3)

result = calc.getResult()
print(result)  # 7
