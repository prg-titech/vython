from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.DVC
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/DVC/vtprop_primitive.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成し、実行
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    v_a1 = dict["v_a1"]
    v_a2 = dict["v_a2"]
    v_b1 = dict["v_b1"]
    assert hasExpectedVT(v_a1, 1)
    assert hasExpectedVT(v_a2, 4)
    assert hasExpectedVT(v_b1, 0)
    assert hasExpectedVT(v_a1 + v_a2, 5)
    assert hasExpectedVT(v_a1 + v_b1, 1)
    assert hasExpectedVT(v_b1 + v_a2, 4)
