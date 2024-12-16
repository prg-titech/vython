from src.transpiler.compiler import Compiler as TC
from helper_func import *
import pytest

@pytest.mark.syntax
def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/syntax/match.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    t = TC(code,"vython").run_fullpath()
    result = t.get_result()['output']
    dict = t.get_dict()

    # 結果を検証
    assert result == "other\nOK\n"
    