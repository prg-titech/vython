from src.syntax.semantics import *

# 評価開始時にヒープに入る情報
boolean_member_list = [
    # &演算
    ["&", VObject("function", VersionTable("bool", 0, False), name = "&", args = ["left", "right"], body = [(lambda left,right:left & right)], partial_args = [])],
    # |演算
    ["|", VObject("function", VersionTable("bool", 0, False), name = "¥", args = ["left", "right"], body = [(lambda left,right:left | right)], partial_args = [])]    
]
