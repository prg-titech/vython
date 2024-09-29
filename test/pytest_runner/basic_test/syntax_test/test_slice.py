from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.syntax
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/slice.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    # 結果を検証
    result1 = dict["result1"]
    result2 = dict["result2"]
    result3 = dict["result3"]
    result4 = dict["result4"]
    assert isSameArray(result1, [4, 5, 6, 7, 8, 9, 10, 11, 12])
    assert isSameArray(result2, [1, 2, 3, 4, 5, 6, 7, 8])
    assert isSameArray(result3, [5, 6, 7])
    assert isSameArray(result4, [3, 5, 7, 9, 11])
    