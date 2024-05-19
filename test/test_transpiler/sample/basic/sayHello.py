# クラス定義
class Person!1:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return "Hello, my name is " + self.name

# クラスのインスタンス生成と属性参照
person1 = Person!1("Alice", 30)
person2 = Person!1("Bob", 25)

# 属性参照とメソッド呼び出し
print(person1.name)      # "Alice"
print(person1.age)       # 30
print(person1.greet())   # "Hello, my name is Alice"

print(person2.name)      # "Bob"
print(person2.age)       # 25
print(person2.greet())   # "Hello, my name is Bob"
