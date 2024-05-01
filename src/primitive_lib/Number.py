from src.syntax.semantics import *

# ヒープに入る情報をそのまま書く
# numberクラスの情報
number_member_list = [
    ["+", VObject("function", VersionTable("number", 0, False), name = "+", args = ["self", "right"], body = [(lambda: self + right)], partial_args = [])]
]

# VObject("class", VersionTable("number", 0, False), name = "number", bases = [], body = {"+",,,?})
    
    