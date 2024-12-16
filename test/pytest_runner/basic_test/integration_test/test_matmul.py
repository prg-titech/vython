from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.integration
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/matmul.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    # 結果を検証
    m = dict["m"]
    assert isSameValue(m.a11, 8)
    assert isSameValue(m.a12, 2)
    assert isSameValue(m.a21, 22)
    assert isSameValue(m.a22, 8)
