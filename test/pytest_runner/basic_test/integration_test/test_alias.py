from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.integration
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/integration/alias.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()
    dict = t.get_dict()

    # 結果を検証
    assert isSameClass(dict["box2"].content, "Apple_v_1")
