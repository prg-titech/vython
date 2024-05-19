from src.syntax.semantics import *

# 評価開始時にヒープに入る情報
vtb = VersionTable("bool", 0, False)
type_b = "bool"
boolean_member_list = [
    # &演算
    ["__and__", VObject("function", VersionTable("bool", 0, False), name = "__and__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left and right))], partial_args = [])],
    # |演算
    ["__or__", VObject("function", VersionTable("bool", 0, False), name = "__or__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left or right))], partial_args = [])],
    # ==演算
    ["__eq__", VObject("function", VersionTable("bool", 0, False), name = "__eq__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left == right))], partial_args = [])],
    # !=演算
    ["__ne__", VObject("function", VersionTable("bool", 0, False), name = "__ne__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left != right))], partial_args = [])],
    # __bool__演算
    ["__bool__", VObject("function", VersionTable("bool", 0, False), name = "__bool__", args = ["self"], body = [(lambda self:self.attributes["value"])])]
]
