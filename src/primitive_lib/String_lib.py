from src.syntax.semantics import *

# 評価開始時にヒープに入る情報
string_member_list = [
    # ==演算
    ["__eq__", VObject("function", VersionTable("string", 0, False), name = "__eq__", args = ["left", "right"], body = [(lambda left,right:left == right)], partial_args = [])],
    # !=演算
    ["__ne__", VObject("function", VersionTable("string", 0, False), name = "__ne__", args = ["left", "right"], body = [(lambda left,right:left != right)], partial_args = [])],
    # <演算
    ["__lt__", VObject("function", VersionTable("string", 0, False), name = "__lt__", args = ["left", "right"], body = [(lambda left,right:left < right)], partial_args = [])],
    # >演算
    ["__gt__", VObject("function", VersionTable("string", 0, False), name = "__gt__", args = ["left", "right"], body = [(lambda left,right:left > right)], partial_args = [])],
    # <=演算
    ["__le__", VObject("function", VersionTable("string", 0, False), name = "__le__", args = ["left", "right"], body = [(lambda left,right:left <= right)], partial_args = [])],
    # >=演算
    ["__ge__", VObject("function", VersionTable("string", 0, False), name = "__ge__", args = ["left", "right"], body = [(lambda left,right:left >= right)], partial_args = [])]
]
