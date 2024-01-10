# 計算結果全体を示すクラス
class Result:
    pass


# 値(式の計算結果)を示すクラス
# 今このクラスを継承する唯一のクラスはObject。（Int値やBool値はないため）
class Value(Result):
    pass


# 値を返さない計算結果（例：文の実行結果）を表すクラス
class Void(Result):
    def __repr__(self):
        return "Void"


# 計算の失敗を表すクラス
# エラーメッセージや例外情報を保持する。
class Failure(Result):
    def __init__(self, message, exception=None):
        self.message = message
        self.exception = exception

    def __repr__(self):
        return f"Failure(message={self.message})"


# オブジェクトを示すクラス
class Object(Value):
    def __init__(self, class_name, **attributes):
        super().__init__()
        self.type_tag = class_name
        self.attributes = attributes

    def __repr__(self):
        return f"Object(type_tag='{self.type_tag}', attributes={self.attributes})"

    def get_attribute(self, attr):
        return self.attributes.get(attr)

    def set_attribute(self, attr, value):
        self.attributes[attr] = value


##########################
### 以下評価環境の定義 ###
##########################


# グローバルな名前環境を示すクラス
# 名前 -> それが指すヒープ環境上の値への参照 の辞書
class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def __str__(self):
        return f"Environment({self.variables}, {self.parent})"

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Name '{name}' is not defined")

    def set(self, name, value):
        self.variables[name] = value


# ヒープ環境を示すクラス
# 番地 -> その番地に格納されている値 の辞書
class Heap:
    def __init__(self):
        self.objects = []

    def __str__(self):
        return f"Heap({self.objects})"

    def allocate(self, obj):
        self.objects.append(obj)
        return len(self.objects) - 1  # オブジェクトの参照としてインデックスを返す

    def get(self, index):
        return self.objects[index]
