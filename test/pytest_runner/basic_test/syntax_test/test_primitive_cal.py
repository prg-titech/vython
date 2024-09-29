from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.syntax
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/primitive_cal.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    # 結果を検証
    assert isSameValue(dict["add_result"], 19)
    assert isSameValue(dict["sub_result"], 11)
    assert isSameValue(dict["mul_result"], 60)
    assert isSameValue(dict["div_result"], 3.75)

    assert isSameValue(dict["concat_result"], "Hello World")

    assert isSameValue(dict["and_result"], False)
    assert isSameValue(dict["or_result"], True)
    assert isSameValue(dict["not_result"], False)
    