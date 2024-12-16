from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.syntax
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/for.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    # 結果を検証
    assert result == "first\nsecond\n0\n1\n2\n3\n4\n5\n6\n7\n8\n9\nsuccessfully ends!\n"
    
