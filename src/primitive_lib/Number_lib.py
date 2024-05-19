from src.syntax.semantics import *

# 評価開始時にヒープに入る情報
vtn = VersionTable("number", 0, False)
vtb = VersionTable("bool", 0, False)
type_n = "number"
type_b = "bool"
number_member_list = [
    # +演算
    ["__add__", VObject("function", VersionTable("number", 0, False), name = "__add__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left+right))], partial_args = [])],
    # -演算
    ["__sub__", VObject("function", VersionTable("number", 0, False), name = "__sub__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left-right))], partial_args = [])],
    # *演算
    ["__mul__", VObject("function", VersionTable("number", 0, False), name = "__mul__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left*right))], partial_args = [])],
    # /演算
    ["__div__", VObject("function", VersionTable("number", 0, False), name = "__div__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left/right))], partial_args = [])],
    # %演算
    ["__mod__", VObject("function", VersionTable("number", 0, False), name = "__mod__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left%right))], partial_args = [])],
    # //演算
    ["__floordiv__", VObject("function", VersionTable("number", 0, False), name = "__floordiv__", args = ["left", "right"], body = [(lambda left,right:VObject(type_n,vtn,value=left//right))], partial_args = [])],
    # ==演算
    ["__eq__", VObject("function", VersionTable("number", 0, False), name = "__eq__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left==right))], partial_args = [])],
    # !=演算
    ["__ne__", VObject("function", VersionTable("number", 0, False), name = "__ne__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left!=right))], partial_args = [])],
    # <演算
    ["__lt__", VObject("function", VersionTable("number", 0, False), name = "__lt__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left<right))], partial_args = [])],
    # >演算
    ["__gt__", VObject("function", VersionTable("number", 0, False), name = "__gt__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left>right))], partial_args = [])],
    # <=演算
    ["__le__", VObject("function", VersionTable("number", 0, False), name = "__le__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left<=right))], partial_args = [])],
    # >=演算
    ["__ge__", VObject("function", VersionTable("number", 0, False), name = "__ge__", args = ["left", "right"], body = [(lambda left,right:VObject(type_b,vtb,value=left>=right))], partial_args = [])],
    # __bool__演算
    ["__bool__", VObject("function", VersionTable("number", 0, False), name = "__bool__", args = ["self"], body = [(lambda self:self.attributes["value"])])]
]
    
    