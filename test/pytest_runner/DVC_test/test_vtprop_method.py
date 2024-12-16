from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.DVC
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/DVC/vtprop_method.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    assert hasExpectedVT(dict["n"], 0)
    assert hasExpectedVT(dict["return_value_from_a2"], 4)
    assert hasExpectedVT(dict["return_value_from_b1"], 0)
