from src.syntax.language import Name, Version

# 計算結果全体を示すクラス
class Result:
    pass


# 値(式の計算結果)を示すクラス
# 今このクラスを継承する唯一のクラスはVObject。（Int値やBool値はないため）
class Value(Result):
    pass


# 値を返さない計算結果（例：文の実行結果）を表すクラス
# こんな値はpythonにはないのでどうするか？Noneは単一のインスタンスで、一度生成されたらずっと使い回せる
# class Void(Result):
#     def __repr__(self):
#         return "Void"


# 計算の失敗を表すクラス
# エラーメッセージや例外情報を保持する。
# 注：まだ計算失敗は未実装。
class Failure(Result):
    def __init__(self, message, exception=None):
        self.message = message
        self.exception = exception

    def __repr__(self):
        return f"Failure(message={self.message})"


# オブジェクトを示すクラス
# 要バージョンテーブル
class VObject(Value):
    def __init__(self, type_tag, **attributes):
        super().__init__()
        self.type_tag = type_tag
        self.attributes = attributes

    def __repr__(self):
        return f"VObject(type_tag='{self.type_tag}', attributes={self.attributes})"

    def get_attribute(self, attr):
        return self.attributes.get(attr)

    def set_attribute(self, attr, value):
        self.attributes[attr] = value


# VersionTableの定義のひな型
# Versiontable操作用のヘルパー関数もここに定義
class VersionTable():
    def __init__(self, version):
        pass
    def modify(self, modname, version):
        pass
    def union(self, vt):
        pass



##########################
### 以下評価環境の定義 ###
##########################


# グローバルな名前環境を示すクラス
# (名前, バージョン) -> それが指すヒープ環境上の値への参照 の辞書
class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.bindings = {}

    def __str__(self):
        return f"Environment({self.bindings}, {self.parent})"

    def get(self, name, version):
        key = None
        if version is not None:
          key = (name, version)
        else:
          key = (name, None)

        if key in self.bindings:
            return self.bindings[key]
        elif self.parent is not None:
            name, version = key
            return self.parent.get(name, version)
        else:
            raise NameError(f"Name '{name}' with version '{version}' is not defined")

    def set(self, name, version, heap_index):
        key = (None, None)
        if isinstance(version, Version):
          key = (name, version.version)
        else:
          key = (name, None)

        self.bindings[key] = heap_index


# ヒープ環境を示すクラス
# 値が生成された順に格納されており、indexがポインタの代わり
class Heap:
    def __init__(self):
        self.objects = []

    def __str__(self):
        indexed_objects_str = ", ".join(
            [f"{index}: {str(obj)}" for index, obj in enumerate(self.objects)]
        )
        return f"Heap([{indexed_objects_str}])"

    def allocate(self, obj):
        self.objects.append(obj)
        return len(self.objects) - 1  # オブジェクトの参照としてインデックスを返す

    def get(self, index):
        return self.objects[index]


# 完全な形式の(参照を含まない)オブジェクトを構成するヘルパー関数
def resolve_heap_object(heap, index, resolved_indices=None):
    if resolved_indices is None:
        resolved_indices = set()

    if index in resolved_indices:
        return index

    obj = heap.get(index)
    resolved_indices.add(index)

    if isinstance(obj, VObject):
        resolved_attributes = {}
        for attr, value in obj.attributes.items():
            attr_name = attr.id if isinstance(attr, Name) else attr  # 属性名を文字列に変換

            if isinstance(value, int) and value not in resolved_indices:
                resolved_attributes[attr_name] = resolve_heap_object(
                    heap, value, resolved_indices
                )
            else:
                resolved_attributes[attr_name] = value
        return VObject(obj.type_tag, **resolved_attributes)
    else:
        return obj
