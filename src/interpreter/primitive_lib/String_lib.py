from src.interpreter.syntax.semantics import *

# 評価開始時にヒープに入る情報
vts = VersionTable("string", 0, False)
type_s = "string"
type_b = "bool"
string_member_list = [
    # 連結演算
    ["__add__", VObject("function", VersionTable("string", 0, False), name = "__add__", args = ["left", "right"], body = [(lambda left,right:VObject(type_s,vts,value=left+right))], partial_args = [])],
    # ==演算
    ["__eq__", VObject("function", VersionTable("string", 0, False), name = "__eq__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left==right))], partial_args = [])],
    # !=演算
    ["__ne__", VObject("function", VersionTable("string", 0, False), name = "__ne__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left!=right))], partial_args = [])],
    # <演算
    ["__lt__", VObject("function", VersionTable("string", 0, False), name = "__lt__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left<right))], partial_args = [])],
    # >演算
    ["__gt__", VObject("function", VersionTable("string", 0, False), name = "__gt__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left>right))], partial_args = [])],
    # <=演算
    ["__le__", VObject("function", VersionTable("string", 0, False), name = "__le__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left<=right))], partial_args = [])],
    # >=演算
    ["__ge__", VObject("function", VersionTable("string", 0, False), name = "__ge__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vts,value=left>=right))], partial_args = [])],
    # __bool__演算
    ["__bool__", VObject("function", VersionTable("string", 0, False), name = "__bool__", args = ["self"], body = [(lambda self:bool(self.attributes["value"]))])]
]
