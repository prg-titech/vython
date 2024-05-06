from src.syntax.semantics import *

# 評価開始時にヒープに入る情報
number_member_list = [
    # +演算
    ["__add__", VObject("function", VersionTable("number", 0, False), name = "__add__", args = ["left", "right"], body = [(lambda left,right:left + right)], partial_args = [])],
    # -演算
    ["__sub__", VObject("function", VersionTable("number", 0, False), name = "__sub__", args = ["left", "right"], body = [(lambda left,right:left - right)], partial_args = [])],
    # *演算
    ["__mul__", VObject("function", VersionTable("number", 0, False), name = "__mul__", args = ["left", "right"], body = [(lambda left,right:left * right)], partial_args = [])],
    # /演算
    ["__div__", VObject("function", VersionTable("number", 0, False), name = "__div__", args = ["left", "right"], body = [(lambda left,right:left / right)], partial_args = [])],
    # %演算
    ["__mod__", VObject("function", VersionTable("number", 0, False), name = "__mod__", args = ["left", "right"], body = [(lambda left,right:left % right)], partial_args = [])],
    # //演算
    ["__floordiv__", VObject("function", VersionTable("number", 0, False), name = "__floordiv__", args = ["left", "right"], body = [(lambda left,right:left // right)], partial_args = [])]
]
    
    