from src.transpiler.compiler import Compiler as TC
from src.interpreter.compiler import Compiler as IC
from src.interpreter.syntax.semantics import *
from test.pytest_runner.forTest import *

def test():
    # テスト用のソースコードを読み込む
    with open("test/sample_program/basic/loop1.py", "r") as f:
        code = f.read()

    # コンパイラのインスタンスを作成
    result_i = IC(code,False).get_result_fullpath()
    result_t = TC(code,False,False).get_result_fullpath()

    # 結果を検証
    assert result_t == "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\n"
